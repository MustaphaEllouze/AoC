from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict
from aoc.tools import Map

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        map = Map(raw_data=self.data)


        patches = defaultdict(list)

        # This double BFS could be grandly optimized
        to_visit = list(map.iterator)
        visited = []
        id = 0
        while to_visit :
            id += 1
            start_case = to_visit.pop(0)
            sub_to_visit = [start_case]
            while sub_to_visit:
                case = sub_to_visit.pop(0)
                if case in visited : continue
                if case in to_visit : to_visit.remove(case)
                visited.append(case)
                sub_to_visit += [
                    e 
                    for e in map.cardinal_neighbours(*case)
                    if map(*e) == map(*case)
                ]
                patches[id].append(case)
        
        if not part2 :
            bordure = {
                c:sum(
                    (
                        neigh is None or map(*neigh) != map(*c) 
                        for neigh in map.cardinal_neighbours(*c, filter_none=False)
                    )
                )
                for plante, cases in patches.items()
                for c in cases
            }

            for plante, cases in patches.items():
                result += len(cases)*sum([bordure[c] for c in cases])

        else:
            sides = defaultdict(int)
            for patch, cases in patches.items():
                edges = defaultdict(list)
                for c in cases:
                    for neigh,dir in zip(
                        (
                            map.up(*c),
                            map.left(*c),
                            map.down(*c),
                            map.right(*c),
                        ) , ('U', 'L', 'D', 'R')):
                        if neigh is None or map(*neigh) != map(*c):
                            match dir:
                                case 'U' : edges[dir].append(c)
                                case 'D' : edges[dir].append(c)
                                case 'L' : edges[dir].append(c)
                                case 'R' : edges[dir].append(c)
                for dir in ('U', 'L', 'D', 'R') : 
                    match dir :
                        case 'U' | 'D' :
                            edges[dir] = sorted(edges[dir])
                            differences = [
                                (l,r) for l,r in zip(edges[dir][:-1], edges[dir][1:])
                                if r[1]-l[1] != 1 or r[0]-l[0] != 0 
                            ]
                        case 'L' | 'R' :
                            edges[dir] = sorted(edges[dir], key=lambda x:(x[1], x[0]))
                            differences = [
                                (l,r) for l,r in zip(edges[dir][:-1], edges[dir][1:])
                                if r[0]-l[0] != 1 or r[1]-l[1] != 0 
                            ]
                    sides[patch] += len(differences)+1
            
            result = sum(len(patches[patch])*sides[patch] for patch in patches)


        return map, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)