from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

            first_list = [
                 int(line.split(' ')[0]) for line in self.data
            ]
            
            second_list = [
                 int(line.split(' ')[-1]) for line in self.data
            ]

            if not part2 :
                result = sum(
                    abs(e1-e2)
                    for e1,e2 in zip(
                        sorted(first_list),
                        sorted(second_list)
                    )
                )
            else:
                 result = sum(
                      second_list.count(e1)*e1
                      for e1 in first_list
                 )

            return None, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
