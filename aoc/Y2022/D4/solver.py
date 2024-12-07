from typing import Any
from aoc.tools import ABCSolver
from aoc.tools.superstring import SuperString

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        for line in self.data:
            a,b,c,d = SuperString(line).split(characters=['-',','])
            a,b,c,d = int(a), int(b), int(c), int(d)
            result += ((a<=c and b>=d) or (c<=a and d>=b)) and (not part2)
            result += (len(set(range(a, b+1)).intersection(set(range(c, d+1))))>0) and (part2)

        return None, result

    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)