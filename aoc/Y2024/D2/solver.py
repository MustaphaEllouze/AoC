from typing import Any
from aoc.tools import ABCSolver

def is_safe(numbers:list[int])->bool:
    differences = [e1-e2 for (e1,e2) in zip(numbers[1:], numbers[:-1])]
    safe1 = all([e>0 for e in differences]) or all([e<0 for e in differences])
    safe2 = all([abs(e)<=3 for e in differences])
    return safe1 and safe2

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
            result = 0
            for report in self.data :
                numbers = [int(e) for e in report.split()]
                if not part2 : 
                    result += is_safe(numbers=numbers)
                if part2 :
                    result += any(
                        [
                            is_safe(numbers[:i] + numbers[i+1:])
                            for i in range(len(numbers))
                        ]
                    ) or is_safe(numbers=numbers)
            return None, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
