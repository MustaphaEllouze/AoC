from typing import Any
from aoc.tools import ABCSolver

def find_largest(numbers:list[int], left:int) -> tuple[int, list[int]] :
    maxi = max(numbers[:-left])
    index = numbers.index(maxi)
    return maxi, numbers[index+1:]

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        result = 0
        left = 1 if not part2 else 11

        for line in self.data :
            numbers = [int(e) for e in line]
            sub_result = 0
            for i in range(left):
                maxi, numbers = find_largest(numbers, left-i)
                sub_result += maxi
                sub_result *= 10
            sub_result += max(numbers)
            result += sub_result

        return None, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
