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

CLASSIFIERS = {}

class Classifier:
    def __init__(
            self,
            name:str,
            check:Checker,
            option_one:str,
            option_two:str) -> None:
        CLASSIFIERS[name] = self
        self.checker = check
        self.o1 = option_one
        self.o2 = option_two

ACCEPTED = Classifier('ACCEPTED', None, None, None)
REFUSED = Classifier('REFUSED', None, None, None)

def classify(part:Part, classifier:Classifier)->bool:
    if classifier is ACCEPTED : return True
    elif classifier is REFUSED : return False
    else:
        if classifier.checker.evaluate(part) : 
            return classify(part, CLASSIFIERS[classifier.o1])
        else:
            return classify(part, CLASSIFIERS[classifier.o2])

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        classifiers = [line for line in self.data if line != '' and line[0]!='{']
        objects = [line for line in self.data if line != '' and line[0]=='{']

        print(
            classify(
                Part(1, 1, 1, 1),
                Classifier(
                    'Hallo',
                    Checker(
                        100, 
                        Operations.LT,
                        Attributes.A,
                    ),
                    option_one = 'REFUSED',
                    option_two = 'ACCEPTED',
                )
            )
        )

        return '0',0
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)