from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        values = [[int(e) for e in line.split()] for line in self.data]

        def predict(linevalue:list[int]):
            current = [e for e in linevalue]
            sublines = [current]
            while not all([e == 0 for e in current]):
                current = [e2-e1 for e1, e2 in zip(current[:-1], current[1:])]
                sublines.append(current)
            sublines = sublines[::-1]
            sublines[0].append(0)
            for slinebas, slinehaut in zip(sublines[:-1], sublines[1:]):
                slinehaut.append(slinehaut[-1]+slinebas[-1])
            return sublines[-1][-1]

        if not part2 : 
            return values, sum([predict(sline) for sline in values])
        if  part2 : 
            return values, sum([predict(sline[::-1]) for sline in values])
    
    def generate_view(self, structure: Any) -> str:
        return structure