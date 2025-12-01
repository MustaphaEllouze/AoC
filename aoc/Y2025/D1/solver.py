from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        result = 0
        start = 50

        data = [
             (1 if line[0]=='R' else -1, int(line[1:]))
             for line in self.data
        ]
        
        for coef, num in data:
            for i in range(num):
                start += coef
                start = start % 100
                if part2 : 
                    if start == 0 : result += 1
            if not part2 : 
                if start == 0 : result += 1

        return None, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
