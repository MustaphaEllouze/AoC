from typing import Any
from aoc.tools import ABCSolver
from aoc.tools import Map

SYMBOLS = ['%', '-', '$', '=', '*', '#', '@', '/', '+', '&']

class Solver(ABCSolver):
    def solve(self, part2: bool = False) -> tuple[Any, str]:
        
        map = Map([list(line) for line in self.data])
        
        startingind = []

        def findnumberfromrandomindex(ind:tuple[int], filter:bool)->int:
            starting = ind
            while map.left(*starting) is not None and map(*map.left(*starting)).isdigit():
                starting = map.left(*starting)
            if not starting in startingind : 
                if filter : startingind.append(starting)
                finishing = starting
                stratstring = map(*finishing)
                while map.right(*finishing) is not None and map(*map.right(*finishing)).isdigit():
                    finishing = map.right(*finishing)
                    stratstring += map(*finishing)
            
                return int(stratstring)
            else:
                return None

        if not part2 : 
            rpart1 = 0
            indsymb = [ind for ind in map.iterator if map(*ind) in SYMBOLS]
            tovisit = [ind for isym in indsymb for ind in map.neighbours(*isym) if map(*ind).isdigit()]
            for ind in tovisit:
                foundnumber = findnumberfromrandomindex(ind, filter=True)
                if foundnumber is not None : rpart1 += foundnumber
            return 'No structure', rpart1
        else:
            rpart2 = 0
            indsymb = [ind for ind in map.iterator if map(*ind)=='*']
            for gear in indsymb:
                startingind = []
                tovisit = [ind for ind in map.neighbours(*gear) if map(*ind).isdigit()]
                numbersgear = [findnumberfromrandomindex(ind, filter=True) for ind in tovisit]
                numbersgear = [e for e in numbersgear if e is not None]
                if len(numbersgear)==2:
                    rpart2 += numbersgear[0]*numbersgear[1]

            return 'No structure', rpart2
    
    def generate_view(self, structure: Any) -> str:
        return str(structure)