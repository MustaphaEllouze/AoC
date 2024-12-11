from typing import Any
from aoc.tools import ABCSolver
from functools import cache

from collections import defaultdict

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

        stones = defaultdict(int)
        for stone in self.data[0].split():
            stones[int(stone)] += 1

        for i in range(25+50*part2):
            new_stones = defaultdict(int)
            for stone, number in stones.items():
                s1, s2 = blink(number=stone)
                if s1: new_stones[s1] += number
                if s2 is not None : new_stones[s2] += number
            stones = new_stones

        return stones, sum([e for e in stones.values()])


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)