from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict

import re

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        crates = defaultdict(list)

        new_lines = []
        moves = []

        for line in self.data_unstripped:
            if not line.strip() : break
            new_lines.append(line[1::4])
        
        for line in self.data:
            if 'move' in line :
                moves.append(line)
        
        for line in new_lines[::-1][1:]:
            for i,c in enumerate(list(line)):
                if c.strip():
                    crates[i+1].append(c.strip())
        
        pattern = re.compile(r'move (\d*) from (\d*) to (\d*)')

        for move in moves:
            qty, src, dest = [
                int(e) 
                for e in re.match(pattern, move).groups()
            ]

            move_this = crates[src][-qty:]
            crates[src] = crates[src][:-qty]
            if not part2:
                crates[dest] += move_this[::-1]
            else:
                crates[dest] += move_this
        
        return None, "".join([crates[i][-1] for i in crates])

    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)