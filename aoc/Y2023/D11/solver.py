from typing import Any
from aoc.tools import ABCSolver, Map

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        universe = Map([list(line) for line in self.data])
        emptyline = [
            i for 
            i,line in enumerate(universe.map)
            if all([e=='.' for e in line])
        ]
        emptycolu = [
            j for 
            j,line in enumerate(universe.map.T)
            if all([e=='.' for e in line])
        ]
        galaxies = [iter for iter in universe.iterator if universe(*iter)=='#']

        result = 0
        for i,g1 in enumerate(galaxies):
            for j,g2 in enumerate(galaxies[i+1:]):
                subr = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
                subr += (1+(1000000-2)*(part2))*sum([1 for c in emptyline if g1[0]<c<g2[0] or g1[0]>c>g2[0]])
                subr += (1+(1000000-2)*(part2))*sum([1 for l in emptycolu if g1[1]<l<g2[1] or g1[1]>l>g2[1]])
                result += subr

        return universe.map, result
    
    def generate_view(self, structure: Any) -> str:
        result  ='\n'
        for line in structure :
            for element in line :
                result += element
            result += '\n'
        return result