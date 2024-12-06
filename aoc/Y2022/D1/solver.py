from typing import Any
from aoc.tools import ABCSolver
from collections import defaultdict

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        elves = defaultdict(int)
        i = 0
        for line in self.data:
            if line.strip() == '' : i+=1
            else: elves[i]+=int(line)

        return None, sum(sorted(elves.values(), reverse=True)[0:1+2*part2])


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)