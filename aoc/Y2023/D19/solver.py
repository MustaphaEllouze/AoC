from typing import Any
from aoc.tools import ABCSolver
from enum import Enum
from dataclasses import dataclass

class Operations(Enum):
    LT = '<'
    GT = '>'
    EQ = '=='

class Attributes(Enum):
    A = 'a'
    X = 'x'
    M = 'm'
    S = 's'

@dataclass
class Part:
    a:int
    x:int
    m:int
    s:int

    @classmethod
    def from_input(cls, input:str):
        x,m,a,s = input.strip('{').strip('}').split(',')
        return Part(
            x = int(x[2:]),
            a = int(a[2:]),
            m = int(m[2:]),
            s = int(s[2:]),
        )

class Checker:
    def __init__(
            self,
            value:int, 
            operation:Operations,
            attribute:Attributes,
        ) -> None:
        self.value = value
        self.operation = operation
        self.attribute = attribute
    
    def evaluate(self, part:Part)->bool:
        partattr = part.__getattribute__(self.attribute.value)
        match self.operation:
            case Operations.LT:
                return partattr<self.value
            case Operations.GT:
                return partattr>self.value
            case Operations.EQ : 
                return partattr==self.value
    
    @classmethod
    def from_input(cls, input:str)->'Checker':
        attribute = input[0]
        operation = input[1]
        number = int(input[2:])
        match attribute:
            case 'a' : 
                _attr = Attributes.A
            case 'm' : 
                _attr = Attributes.M
            case 'x' : 
                _attr = Attributes.X
            case 's' : 
                _attr = Attributes.S
        match operation:
            case '<':
                _oper = Operations.LT
            case '>':
                _oper = Operations.GT
            case '=':
                _oper = Operations.EQ
        return Checker(value=number, operation=_oper, attribute=_attr)


class Classifier:
    CLASSIFIERS = {}
    COUNTER_CLASSIFIER = 1
    def __init__(
            self,
            name:str,
            check:Checker,
            option_one:str,
            option_two:str) -> None:
        Classifier.CLASSIFIERS[name] = self
        self.name = name
        self.checker = check
        self.o1 = option_one
        self.o2 = option_two
    
    @classmethod
    def from_input(cls, input:str)->'Classifier':
        # format : px{a<2006:qkq,m>2090:A,rfg}
        acco_idx = input.index('{')
        deuxpts_idx = input.index(':')
        virg_idx = input.index(',')
        name = input[0:acco_idx]
        checking_sequence = input[acco_idx+1:deuxpts_idx]
        checker = Checker.from_input(input=checking_sequence)
        child1 = input[deuxpts_idx+1:virg_idx]
        name_child1 = child1
        child2 = input[virg_idx+1:-1]
        name_child2 = child2
        if ':' in child1 :
            Classifier.COUNTER_CLASSIFIER += 1 
            child1 = f'MEE{Classifier.COUNTER_CLASSIFIER}'+'{'+child1+'}'
            child1_c = Classifier.from_input(child1)
            name_child1 = f'MEE{Classifier.COUNTER_CLASSIFIER}'
        if ':' in child2 :
            Classifier.COUNTER_CLASSIFIER += 1 
            child2 = f'MEE{Classifier.COUNTER_CLASSIFIER}'+'{'+child2+'}'
            child2_c = Classifier.from_input(child2)
            name_child2 = f'MEE{Classifier.COUNTER_CLASSIFIER}'
        
        if name_child1 == 'A':
            name_child1 = 'ACCEPTED'
        if name_child1 == 'R':
            name_child1 = 'REFUSED'
        if name_child2 == 'A':
            name_child2 = 'ACCEPTED'
        if name_child2 == 'R':
            name_child2 = 'REFUSED'
        
        return Classifier(
            name=name, 
            check=checker,
            option_one=name_child1,
            option_two=name_child2,
        )

ACCEPTED = Classifier('ACCEPTED', None, None, None)
REFUSED = Classifier('REFUSED', None, None, None)

def classify(part:Part, classifier:Classifier)->bool:
    # print(part)
    if classifier is ACCEPTED : return True
    elif classifier is REFUSED : return False
    else:
        if classifier.checker.evaluate(part) : 
            # print(classifier.o1)
            return classify(part, Classifier.CLASSIFIERS[classifier.o1])
        else:
            # print(classifier.o2)
            return classify(part, Classifier.CLASSIFIERS[classifier.o2])

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        classifiers = [Classifier.from_input(line) for line in self.data if line != '' and line[0]!='{']
        objects = [
            Part.from_input(input=line) 
            for line in self.data 
            if line != '' and line[0]=='{'
        ]

        in_classifier = Classifier.CLASSIFIERS['in']

        accepted = [o for o in objects if classify(part=o, classifier=in_classifier)]

        return '0',sum([o.a+o.m+o.x+o.s for o in accepted])
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)