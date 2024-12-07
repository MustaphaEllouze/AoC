from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        let = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        letters = {
            k:i+1
            for i,k in enumerate(let)
        }

        if not part2 :
            for line in self.data:
                result += letters[
                    list(set(line[:len(line)//2]).intersection(set(line[len(line)//2:])))[0]
                ]
        else:
            for l1,l2,l3 in zip(self.data[0::3], self.data[1::3], self.data[2::3]):
                result += letters[
                    list(set(l1).intersection(set(l2)).intersection(set(l3)))[0]
                ]

        return None, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)