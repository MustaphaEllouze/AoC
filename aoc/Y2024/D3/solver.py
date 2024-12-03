from typing import Any
from aoc.tools import ABCSolver

import re

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        data = "".join(self.data)
        matched = re.finditer(
            pattern=r'mul\(\d*\,\d*\)',
            string=data,
        )

        dos = re.finditer(
            pattern=r'do\(\)',
            string=data
        )

        index_dos = [d.start(0) for d in dos]

        donts = re.finditer(
            pattern=r'don\'t\(\)',
            string=data
        )
        
        index_donts = [d.start(0) for d in donts]

        for match in matched:
            numbers = match.group(0)[4:-1].split(',')
            if not part2:
                result += int(numbers[0])*int(numbers[1])
            if part2:
                index = match.start(0)
                dos_sliced = [e for e in index_dos if e<index]
                donts_sliced = [e for e in index_donts if e<index]
                if max(dos_sliced, default=1)>max(donts_sliced, default=0):
                    result += int(numbers[0])*int(numbers[1])

        return None, result

    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)