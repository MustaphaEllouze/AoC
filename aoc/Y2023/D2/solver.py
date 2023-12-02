from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        games = [line for line in self.data]

        result = []
        resultpart2 = []

        for game in games :
            idgame = game.split(':')[0].split(' ')[1]
            sets = game.split(':')[1].split(';')
            nb_blue = 0
            nb_green = 0
            nb_red = 0
            for s in sets:
                balls = s.split(',')
                for sb in balls :
                    if 'blue' in sb :
                        nb_blue = max(nb_blue, int(sb.split('blue')[0]))
                    if 'red' in sb :
                        nb_red = max(nb_red, int(sb.split('red')[0]))
                    if 'green' in sb :
                        nb_green = max(nb_green, int(sb.split('green')[0]))
            
            if nb_blue<=14 and nb_red<=12 and nb_green<=13:
                result.append(int(idgame))
            
            resultpart2.append(nb_blue*nb_green*nb_red)

        if not part2 : 
            return 'No structure', sum(result)
        else:
            return 'No structure', sum(resultpart2)
    
    def generate_view(self, structure: Any) -> str:
        return 'No view'