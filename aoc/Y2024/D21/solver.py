from typing import Any
from aoc.tools import ABCSolver
from functools import lru_cache
from itertools import product

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
    def __init__(self, start_pos:str='A'):
        self.current = start_pos
    def move_to(self, end:str)->list[str]:
        old_cur = self.current
        self.current = end
        return convert_code(old_cur, end)

class Directional:
    #     +---+---+
    #     | ^ | A |
    # +---+---+---+
    # | < | v | > |
    # +---+---+---+
    def __init__(self):
        self.current = 'A'
    def move_to(self, end:str)->list[str]:
        old_cur = self.current
        self.current = end
        return convert_directional(old_cur, end)

def convert_code(start:str, end:str)->list[str]:
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
    
def convert_directional(start:str, end:str)->list[str]:
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

# def transform_input_directional(input:str)->str:


# @lru_cache
# def solve(input:str, layers:int):
#     if layers == 0 : return len(input)
#     sub_inputs = [e+'A' for e in input.split('A') if e != '']
#     transformed_sub_inputs = [
#         transform_input_directional(e)
#         for e in sub_inputs
#     ]

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        pads = [Code()]
        # for _ in range(2+23*part2) :
            # pads.append(Directional()) 

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