from typing import Any
from aoc.tools import ABCSolver
from enum import Enum
from dataclasses import dataclass
from collections import defaultdict

ACCEPTED_s = 'ACCEPTED'
REFUSED_s = 'REFUSED'

class Operations(Enum):
    LT = '<'
    GT = '>'
    EQ = '=='

def other_operations(ope:Operations):
    match ope:
        case Operations.LT : return (Operations.EQ, Operations.GT)
        case Operations.GT : return (Operations.EQ, Operations.LT)
        case Operations.EQ : return (Operations.LT, Operations.GT)

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
    
    def __str__(self) -> str:
        return f'{self.attribute.value}{self.operation.value}{self.value}'
    
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
            name_child1 = child1_c.name
        if ':' in child2 :
            Classifier.COUNTER_CLASSIFIER += 1 
            child2 = f'MEE{Classifier.COUNTER_CLASSIFIER}'+'{'+child2+'}'
            child2_c = Classifier.from_input(child2)
            name_child2 = child2_c.name
        
        if name_child1 == 'A':
            name_child1 = ACCEPTED_s
        if name_child1 == 'R':
            name_child1 = REFUSED_s
        if name_child2 == 'A':
            name_child2 = ACCEPTED_s
        if name_child2 == 'R':
            name_child2 = REFUSED_s
        
        return Classifier(
            name=name, 
            check=checker,
            option_one=name_child1,
            option_two=name_child2,
        )

ACCEPTED = Classifier(ACCEPTED_s, None, None, None)
REFUSED = Classifier(REFUSED_s, None, None, None)

def classify(part:Part, classifier:Classifier, verbose:bool=False)->bool:
    if classifier is ACCEPTED : 
        if verbose : print('-----------> ACCEPTED')
        return True
    elif classifier is REFUSED : 
        if verbose : print('-----------> REFUSED')
        return False
    else:
        if verbose : print('Classifying',part,'with', classifier.name, str(classifier.checker),classifier.o1, classifier.o2)
        if classifier.checker.evaluate(part) : 
            if verbose : print('    Now classifying',part,'with', classifier.o1)
            return classify(part, Classifier.CLASSIFIERS[classifier.o1])
        else:
            if verbose : print('    Now classifying',part,'with', classifier.o2)
            return classify(part, Classifier.CLASSIFIERS[classifier.o2])

@dataclass
class XMASrange:
    x_min:int
    x_max:int
    m_min:int
    m_max:int
    a_min:int
    a_max:int
    s_min:int
    s_max:int

    def cut_with_x(self, x_value:int, operation:Operations):
        match operation:
            case Operations.LT : 
                if self.x_min<x_value:
                    return XMASrange(
                        x_min=self.x_min,
                        x_max=min(x_value-1, self.x_max),
                        m_min=self.m_min,
                        m_max=self.m_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None
            case Operations.GT :
                if self.x_max>x_value:
                    return XMASrange(
                        x_min=max(self.x_min, x_value+1),
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None
            case Operations.EQ :
                if self.x_min<=x_value<=self.x_max :
                    return XMASrange(
                        x_min=x_value,
                        x_max=x_value,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None

    def cut_with_m(self, m_value:int, operation:Operations):
        match operation:
            case Operations.LT : 
                if self.m_min<m_value:
                    return XMASrange(
                        m_min=self.m_min,
                        m_max=min(m_value-1, self.m_max),
                        x_min=self.x_min,
                        x_max=self.x_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None
            case Operations.GT :
                if self.m_max>m_value:
                    return XMASrange(
                        m_min=max(self.m_min, m_value+1),
                        m_max=self.m_max,
                        x_min=self.x_min,
                        x_max=self.x_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None
            case Operations.EQ :
                if self.m_min<=m_value<=self.m_max :
                    return XMASrange(
                        m_min=m_value,
                        m_max=m_value,
                        x_min=self.x_min,
                        x_max=self.x_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None

    def cut_with_a(self, a_value:int, operation:Operations):
        match operation:
            case Operations.LT : 
                if self.a_min<a_value:
                    return XMASrange(
                        a_min=self.a_min,
                        a_max=min(a_value-1, self.a_max),
                        x_min=self.x_min,
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None
            case Operations.GT :
                if self.a_max>a_value:
                    return XMASrange(
                        a_min=max(self.a_min, a_value+1),
                        a_max=self.a_max,
                        x_min=self.x_min,
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None
            case Operations.EQ :
                if self.a_min<=a_value<=self.a_max :
                    return XMASrange(
                        a_min=a_value,
                        a_max=a_value,
                        x_min=self.x_min,
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        s_min=self.s_min,
                        s_max=self.s_max,
                    )
                else:
                    return None

    def cut_with_s(self, s_value:int, operation:Operations):
        match operation:
            case Operations.LT : 
                if self.s_min<s_value:
                    return XMASrange(
                        s_min=self.s_min,
                        s_max=min(s_value-1, self.s_max),
                        x_min=self.x_min,
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                    )
                else:
                    return None
            case Operations.GT :
                if self.s_max>s_value:
                    return XMASrange(
                        s_min=max(self.s_min, s_value+1),
                        s_max=self.s_max,
                        x_min=self.x_min,
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                    )
                else:
                    return None
            case Operations.EQ :
                if self.s_min<=s_value<=self.s_max :
                    return XMASrange(
                        s_min=s_value,
                        s_max=s_value,
                        x_min=self.x_min,
                        x_max=self.x_max,
                        m_min=self.m_min,
                        m_max=self.m_max,
                        a_min=self.a_min,
                        a_max=self.a_max,
                    )
                else:
                    return None

    def nb_combinations(self):
        return (self.x_max-self.x_min+1)*(self.m_max-self.m_min+1)*(self.a_max-self.a_min+1)*(self.s_max-self.s_min+1)

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        classifiers = [Classifier.from_input(line) for line in self.data if line != '' and line[0]!='{']
        objects = [
            Part.from_input(input=line) 
            for line in self.data 
            if line != '' and line[0]=='{'
        ]

        in_classifier = Classifier.CLASSIFIERS['in']

        if not part2 : 
            accepted = [o for o in objects if classify(part=o, classifier=in_classifier)]

            return 'No structure',sum([o.a+o.m+o.x+o.s for o in accepted])

        else:
            result = defaultdict(list)
            result['in'] = [XMASrange(1,4000,1,4000,1,4000,1,4000)]
            while not set(result.keys()).issubset(set([ACCEPTED_s, REFUSED_s])):
                list_keys = [k for k in result.keys() if k not in [ACCEPTED_s, REFUSED_s]]
                assert len(list_keys)>0
                next_key = list_keys[0]

                current_ranges:list[XMASrange]= result.pop(next_key)

                current_classifier:Classifier = Classifier.CLASSIFIERS[next_key]
                true_child = current_classifier.o1
                false_child = current_classifier.o2
                current_checker = current_classifier.checker
                attribute, operation, value = (
                    current_checker.attribute,
                    current_checker.operation,
                    current_checker.value,
                )
                oth_ope1, oth_ope2 = other_operations(operation)
                for range in current_ranges : 
                    if range is None : continue
                    match attribute :
                        case Attributes.X :
                            result[true_child].append(
                                range.cut_with_x(value, operation)
                            )
                            result[false_child].append(
                                range.cut_with_x(value, oth_ope1)
                            )
                            result[false_child].append(
                                range.cut_with_x(value, oth_ope2)
                            )
                        case Attributes.M :
                            result[true_child].append(
                                range.cut_with_m(value, operation)
                            )
                            result[false_child].append(
                                range.cut_with_m(value, oth_ope1)
                            )
                            result[false_child].append(
                                range.cut_with_m(value, oth_ope2)
                            )
                        case Attributes.A :
                            result[true_child].append(
                                range.cut_with_a(value, operation)
                            )
                            result[false_child].append(
                                range.cut_with_a(value, oth_ope1)
                            )
                            result[false_child].append(
                                range.cut_with_a(value, oth_ope2)
                            )
                        case Attributes.S :
                            result[true_child].append(
                                range.cut_with_s(value, operation)
                            )
                            result[false_child].append(
                                range.cut_with_s(value, oth_ope1)
                            )
                            result[false_child].append(
                                range.cut_with_s(value, oth_ope2)
                            )

                print(set(result.keys()))
            result = sum(
                [
                    the_range.nb_combinations() 
                    for the_range in result['ACCEPTED'] 
                    if the_range is not None
                ]
            )
            return 'No structure', result
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)