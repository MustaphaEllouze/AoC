from typing import Any
from aoc.tools import ABCSolver
from collections import defaultdict

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        transf = {
            'A' : 'R', 'X' : 'R',
            'B' : 'P', 'Y' : 'P',
            'C' : 'S', 'Z' : 'S',
        }

        other = [transf[line.split(' ')[0]] for line in self.data]
        me = [transf[line.split(' ')[1]] for line in self.data]
        me2 = [line.split(' ')[1] for line in self.data]

        
        for o,m,m2 in zip(other,me,me2):
            if not part2 :
                result += 1*(m=='R')+2*(m=='P')+3*(m=='S')
                result += 3*(o==m)
                result += 6*(o=='R' and m=='P')+6*(o=='P' and m=='S')+6*(o=='S' and m=='R')
            else:
                result += 3*(m2=='Y')+6*(m2=='Z')

                result += 1*(o=='R' and m2=='Y')
                result += 1*(o=='P' and m2=='X')
                result += 1*(o=='S' and m2=='Z')
                
                result += 2*(o=='P' and m2=='Y')
                result += 2*(o=='S' and m2=='X')
                result += 2*(o=='R' and m2=='Z')
                
                result += 3*(o=='S' and m2=='Y')
                result += 3*(o=='R' and m2=='X')
                result += 3*(o=='P' and m2=='Z')


        return None, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)