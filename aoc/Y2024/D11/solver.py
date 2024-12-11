from typing import Any
from aoc.tools import ABCSolver
from functools import cache

@cache
def blink(number:int)->tuple[int,int]:
    if number == 0 :
        return 1, None
    elif len(str(number))%2 == 0:
        return int(str(number)[:len(str(number))//2]), int(str(number)[len(str(number))//2:])
    else:
        return 2024*number, None

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        stones = [int(e) for e in self.data[0].split()]

        for i in range(25):
            new_stones = []
            for stone in stones:
                s1, s2 = blink(number=stone)
                new_stones.append(s1)
                if s2 is not None : new_stones.append(s2)
            stones = new_stones
                
        return stones, len(stones)


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)