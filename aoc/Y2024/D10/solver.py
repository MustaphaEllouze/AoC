from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        map = Map(raw_data=self.data, conversion_int=True)

        if not part2 : initial_positions = [(e, 0) for e in map.findall(value=0)]
        if part2 :initial_positions = [(e, 0, (e,)) for e in map.findall(value=0)]

        while initial_positions :
            to_visit = [initial_positions.pop(0)]
            visited = []

            while to_visit :
                if not part2 : 
                    pos, val = to_visit.pop(0)
                    if pos in visited : continue
                    visited.append(pos)
                if part2 : 
                    pos, val, path = to_visit.pop(0)
                    if path in visited : continue
                    visited.append(path)
                if val == 9 : result += 1
                for n in map.cardinal_neighbours(*pos) :
                    if map(*n) == val + 1 : 
                        if not part2 : to_visit.append((n, val+1))
                        if part2 : to_visit.append((n, val+1, path+(n,)))
        
        return map, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)