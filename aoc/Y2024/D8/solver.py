from typing import Any
from aoc.tools import ABCSolver
from aoc.tools import Map

from collections import defaultdict
from itertools import combinations

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        map = Map(raw_data=self.data)
        antennas : dict[str, list[tuple[int, int]]] = defaultdict(list)
        antinodes : dict[str, list[tuple[int, int]]] = defaultdict(list)

        for cell in map.iterator:
            value = map(*cell)
            if value != '.':
                antennas[value].append(cell)
        
        for freq, positions in antennas.items():
            for a1, a2 in combinations(positions, 2):
                vector = (a2[0]-a1[0], a2[1]-a1[1])
                if part2 : 
                    disable_self = False
                    factor_len = max(map.height//vector[0], map.width//vector[1])+1
                else:
                    disable_self = True
                    factor_len = 2

                potentials1 = [
                    (a2[0]+i*vector[0], a2[1]+i*vector[1])
                    for i in range(int(disable_self), factor_len)
                ]
                potentials2 = [
                    (a1[0]-i*vector[0], a1[1]-i*vector[1])
                    for i in range(int(disable_self), factor_len)
                ]
                for pot in potentials1+potentials2:
                    if map(*pot) : antinodes[freq].append(pot)

        
        to_prune = []
        for positions in antinodes.values():
            to_prune += positions
        
        for pos in set(to_prune):
            map.map[*pos] = '#'
        
        return map, len(set(to_prune))


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)