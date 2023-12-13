from typing import Any
from aoc.tools import ABCSolver, Map

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        # Parsing
        maps = []
        map = []
        for line in self.data :
            if line == '':
                maps.append(map)
                map = []
            else:
                map.append(line)
        maps.append(map)

        for i,map in enumerate(maps) : 
            maps[i] = Map([list(e) for e in map])

        # Solution
        result = 0
        for map in maps : 
            # On trouve pour chaque ligne l'ensemble des couples de valeurs égales
            couples_col = [
                [
                    i+1 
                    for i in range(len(sub)-1)
                    if all([(x1==x2) for x1,x2 in zip(sub[i::-1],sub[i+1:])])
                ]
                for sub in map.map
            ]
            couples_lin = [
                [
                    i+1 
                    for i in range(len(sub)-1)
                    if all([(x1==x2) for x1,x2 in zip(sub[i::-1],sub[i+1:])])
                ]
                for sub in map.map.T
            ]

            if not part2 : 
                set_col = [i+1 for i in range(len(map.map[0])) if sum([i+1 in cc for cc in couples_col])==len(couples_col)]
                set_lin = [i+1 for i in range(len(map.map)) if sum([i+1 in cc for cc in couples_lin])==len(couples_lin)]
            else:
                set_col = [i+1 for i in range(len(map.map[0])) if sum([i+1 in cc for cc in couples_col])==len(couples_col)-1]
                set_lin = [i+1 for i in range(len(map.map)) if sum([i+1 in cc for cc in couples_lin])==len(couples_lin)-1]

            if set_col : result += set_col[0]
            if set_lin : result += 100*set_lin[0]

        return 'No structure', result
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)