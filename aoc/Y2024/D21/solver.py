from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map
from collections import defaultdict
from itertools import product

class CodeSolver:
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    def __init__(self):
        self.current = 'A'
    def move(self, command:str)->str:
        match command:
            case '>' : 
                match self.current:
                    case 'A' : raise NotImplementedError()
                    case '0' : self.current = 'A'
                    case '1' : self.current = '2'
                    case '2' : self.current = '3'
                    case '3' : raise NotImplementedError()
                    case '4' : self.current = '5'
                    case '5' : self.current = '6'
                    case '6' : raise NotImplementedError()
                    case '7' : self.current = '8'
                    case '8' : self.current = '9'
                    case '9' : raise NotImplementedError()
            case '<' : 
                match self.current:
                    case 'A' : self.current = '0'
                    case '0' : raise NotImplementedError()
                    case '1' : raise NotImplementedError()
                    case '2' : self.current = '1'
                    case '3' : self.current = '2'
                    case '4' : raise NotImplementedError()
                    case '5' : self.current = '4'
                    case '6' : self.current = '5'
                    case '7' : raise NotImplementedError()
                    case '8' : self.current = '7'
                    case '9' : self.current = '8'
            case '^' : 
                match self.current:
                    case 'A' : self.current = '3'
                    case '0' : self.current = '2'
                    case '1' : self.current = '4'
                    case '2' : self.current = '5'
                    case '3' : self.current = '6'
                    case '4' : self.current = '7'
                    case '5' : self.current = '8'
                    case '6' : self.current = '9'
                    case '7' : raise NotImplementedError()
                    case '8' : raise NotImplementedError()
                    case '9' : raise NotImplementedError()
            case 'v' : 
                match self.current:
                    case 'A' : raise NotImplementedError()
                    case '0' : raise NotImplementedError()
                    case '1' : raise NotImplementedError()
                    case '2' : self.current = '0'
                    case '3' : self.current = 'A'
                    case '4' : self.current = '1'
                    case '5' : self.current = '2'
                    case '6' : self.current = '3'
                    case '7' : self.current = '4'
                    case '8' : self.current = '5'
                    case '9' : self.current = '6'
            case 'A' : return self.current
        return ''

class DirectionalSolver:
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    def __init__(self):
        self.current = 'A'
    def move(self, command:str)->str:
        match command:
            case '>' : 
                match self.current:
                    case '^' : self.current = 'A'
                    case 'A' : raise NotImplementedError()
                    case '<' : self.current = 'v'
                    case 'v' : self.current = '>'
                    case '>' : raise NotImplementedError()
            case '<' : 
                match self.current:
                    case '^' : raise NotImplementedError()
                    case 'A' : self.current = '^'
                    case '<' :raise NotImplementedError()
                    case 'v' : self.current = '<'
                    case '>' : self.current = 'v'
            case '^' : 
                match self.current:
                    case '^' : raise NotImplementedError()
                    case 'A' : raise NotImplementedError()
                    case '<' : raise NotImplementedError()
                    case 'v' : self.current = '^'
                    case '>' : self.current = 'A'
            case 'v' : 
                match self.current:
                    case '^' : self.current = 'v'
                    case 'A' : self.current = '>'
                    case '<' : raise NotImplementedError()
                    case 'v' : raise NotImplementedError()
                    case '>' : raise NotImplementedError()
            case 'A' : return self.current
        return ''

class Code:
    # +---+---+---+
    # | 7 | 8 | 9 |
    # +---+---+---+
    # | 4 | 5 | 6 |
    # +---+---+---+
    # | 1 | 2 | 3 |
    # +---+---+---+
    #     | 0 | A |
    #     +---+---+
    @classmethod
    def convert(cls, start:str,end:str)->list[str]:
        match start:
            case 'A' : 
                match end:
                    case 'A' : return ['']
                    case '0' : return ['<']
                    case '1' : return ['^<<'] # impossible other
                    case '2' : return ['^<', '<^']
                    case '3' : return ['^']
                    case '4' : return ['^^<<']# impossible other
                    case '5' : return ['^^<', '<^^']
                    case '6' : return ['^^']
                    case '7' : return ['^^^<<']# impossible other
                    case '8' : return ['^^^<', '<^^^']
                    case '9' : return ['^^^']
            case '0' :  
                match end:
                    case 'A' : return ['>']
                    case '0' : return ['']
                    case '1' : return ['^<']# impossible other
                    case '2' : return ['^']
                    case '3' : return ['^>', '>^']
                    case '4' : return ['^^<']# impossible other
                    case '5' : return ['^^']
                    case '6' : return ['^^>', '>^^']
                    case '7' : return ['^^^<']# impossible other
                    case '8' : return ['^^^']
                    case '9' : return ['^^^>', '>^^^']
            case '1' :  
                match end:
                    case 'A' : return ['>>v']# impossible other
                    case '0' : return ['>v']# impossible other
                    case '1' : return ['']
                    case '2' : return ['>']
                    case '3' : return ['>>']
                    case '4' : return ['^']
                    case '5' : return ['^>', '>^']
                    case '6' : return ['^>>', '>>^']
                    case '7' : return ['^^']
                    case '8' : return ['^^>', '>^^']
                    case '9' : return ['^^>>', '>>^^']
            case '2' :  
                match end:
                    case 'A' : return ['>v', 'v>']
                    case '0' : return ['v']
                    case '1' : return ['<']
                    case '2' : return ['']
                    case '3' : return ['>']
                    case '4' : return ['^<', '<^']
                    case '5' : return ['^']
                    case '6' : return ['^>', '>^']
                    case '7' : return ['^^<', '<^^']
                    case '8' : return ['^^']
                    case '9' : return ['^^>', '>^^']
            case '3' :  
                match end:
                    case 'A' : return ['v']
                    case '0' : return ['v<', '<v']
                    case '1' : return ['<<']
                    case '2' : return ['<']
                    case '3' : return ['']
                    case '4' : return ['^<<', '<<^']
                    case '5' : return ['^<', '<^']
                    case '6' : return ['^']
                    case '7' : return ['^^<<', '<<^^']
                    case '8' : return ['^^<', '<^']
                    case '9' : return ['^^']
            case '4' :  
                match end:
                    case 'A' : return ['>>vv']# impossible other
                    case '0' : return ['>vv']# impossible other
                    case '1' : return ['v']
                    case '2' : return ['>v', 'v>']
                    case '3' : return ['>>v', 'v>>']
                    case '4' : return ['']
                    case '5' : return ['>']
                    case '6' : return ['>>']
                    case '7' : return ['^']
                    case '8' : return ['^>', '>^']
                    case '9' : return ['^>>', '>>^']
            case '5' :  
                match end:
                    case 'A' : return ['>vv', 'vv>']
                    case '0' : return ['vv']
                    case '1' : return ['v<', '<v']
                    case '2' : return ['v']
                    case '3' : return ['v>', '>v']
                    case '4' : return ['<']
                    case '5' : return ['']
                    case '6' : return ['>']
                    case '7' : return ['^<', '<^']
                    case '8' : return ['^']
                    case '9' : return ['^>', '>^']
            case '6' :  
                match end:
                    case 'A' : return ['vv']
                    case '0' : return ['vv<', '<vv']
                    case '1' : return ['v<<', '<<v']
                    case '2' : return ['v<', '<v']
                    case '3' : return ['v']
                    case '4' : return ['<<']
                    case '5' : return ['<']
                    case '6' : return ['']
                    case '7' : return ['^<<', '<<^']
                    case '8' : return ['^<', '<^']
                    case '9' : return ['^']
            case '7' :  
                match end:
                    case 'A' : return ['>>vvv']# impossible other
                    case '0' : return ['>vvv']# impossible other
                    case '1' : return ['vv']
                    case '2' : return ['vv>', '>vv']
                    case '3' : return ['vv>>', '>>vv']
                    case '4' : return ['v']
                    case '5' : return ['v>', '>v']
                    case '6' : return ['v>>', '>>v']
                    case '7' : return ['']
                    case '8' : return ['>']
                    case '9' : return ['>>']
            case '8' :  
                match end:
                    case 'A' : return ['>vvv', 'vvv>']
                    case '0' : return ['vvv']
                    case '1' : return ['vv<', '<vv']
                    case '2' : return ['vv']
                    case '3' : return ['vv>', '>vv']
                    case '4' : return ['v<', '<v']
                    case '5' : return ['v']
                    case '6' : return ['v>', '>v']
                    case '7' : return ['<']
                    case '8' : return ['']
                    case '9' : return ['>']
            case '9' :  
                match end:
                    case 'A' : return ['vvv']
                    case '0' : return ['vvv<', '<vvv']
                    case '1' : return ['vv<<', '<<vv']
                    case '2' : return ['vv<', '<vv']
                    case '3' : return ['vv']
                    case '4' : return ['v<<', '<<v']
                    case '5' : return ['v<', '<v']
                    case '6' : return ['v']
                    case '7' : return ['<<']
                    case '8' : return ['<']
                    case '9' : return ['']
    def __init__(self, start_pos:str='A'):
        self.current = start_pos
    def move_to(self, end:str)->list[str]:
        old_cur = self.current
        self.current = end
        return Code.convert(old_cur, end)

class Directional:
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    @classmethod
    def convert(cls, start:str, end:str)->list[str]:
        match start:
            case '^' :
                match end:
                    case '^' : return ['']
                    case 'A' : return ['>']
                    case '<' : return ['v<']# impossible other
                    case 'v' : return ['v']
                    case '>' : return ['v>', '>v']
            case 'A' :
                match end:
                    case '^' : return ['<']
                    case 'A' : return ['']
                    case '<' : return ['v<<']# impossible other
                    case 'v' : return ['v<', '<v']
                    case '>' : return ['v']
            case '<' :
                match end:
                    case '^' : return ['>^']# impossible other
                    case 'A' : return ['>>^']# impossible other
                    case '<' : return ['']
                    case 'v' : return ['>']
                    case '>' : return ['>>']
            case 'v' :
                match end:
                    case '^' : return ['^']
                    case 'A' : return ['^>', '>^']
                    case '<' : return ['<']
                    case 'v' : return ['']
                    case '>' : return ['>']
            case '>' :
                match end:
                    case '^' : return ['<^', '^<']
                    case 'A' : return ['^']
                    case '<' : return ['<<']
                    case 'v' : return ['<']
                    case '>' : return ['']
    def __init__(self):
        self.current = 'A'
    def move_to(self, end:str)->list[str]:
        old_cur = self.current
        self.current = end
        return Directional.convert(old_cur, end)

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        pads = [Code()]
        for _ in range(2+23*part2) :
            pads.append(Directional()) 

        # checker_dir1 = DirectionalSolver()
        # checker_dir2 = DirectionalSolver()
        # checker_pad = CodeSolver()

        for code1 in self.data:
            res = [code1]
            for pad in pads :
                res = [
                    subsub 
                    for sub_res in res
                    for subsub in ['A'.join(e)+'A' for e in product(*[pad.move_to(end=c) for c in sub_res])]
                ]
                min_length = min([len(e) for e in res])
                res = [e for e in res if len(e)==min_length]
                
            shortest = min(res, key= lambda x:len(x))
            print(shortest)
            result += len(shortest)*int("".join(e for e in code1 if e.isdigit()))

        return None, result
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)