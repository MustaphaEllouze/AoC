from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
        directions = list(self.data[0])
        cells = {
            line[0:3]:{'L':line[7:10], 'R':line[12:15]}
            for line in self.data[2:]
        }

        if not part2 : 
            step = 0
            current = 'AAA'
            while current != 'ZZZ':
                current = cells[current][directions[step%len(directions)]]
                step += 1
            
            return cells, step
        else:
            import math
            steps=[]
            currents = [start for start in cells if start[2]=='A']
            for c in currents : 
                cc = c
                step = 0
                while cc[2]!='Z' : 
                    cc = cells[cc][directions[step%len(directions)]]
                    step += 1
                steps.append(step)
            result = steps[0]
            for s in steps[1:] : result = int((result*s)/math.gcd(result, s))

            return cells, result
    
    def generate_view(self, structure: Any) -> str:
        return structure