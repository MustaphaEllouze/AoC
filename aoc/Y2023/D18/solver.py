from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        data = [
            tuple(line.split())
            for line in self.data
        ]
        points = [(0,0)]


        nb_boundary = 0

        def create_new_pt(instruction, number, x, y):
            match instruction :
                case 'R' : npt = (y, x+int(number))
                case 'U' : npt = (y-int(number), x)
                case 'D' : npt = (y+int(number), x)
                case 'L' : npt = (y, x-int(number))
            return npt

        # construction
        matching_coldir = {0:'R',1:'D',2:'L',3:'U'}
        for instruction, number, color in data :
            y,x = points[-1]
            if not part2 : 
                points.append(create_new_pt(instruction, number, x, y))
                nb_boundary += int(number)
            else:
                points.append(create_new_pt(matching_coldir[int(color[-2])],int(color[2:-2],16), x, y))
                nb_boundary += int(color[2:-2],16)
        
        result = 0
        for p1, p2 in zip(points, points[1:]+points[:1]):
            p10, p11, p20, p21 = p1[0], p1[1], p2[0], p2[1]
            result += (p10*p21-p11*p20)

        result = abs(result/2)
        
        return 'No structure', result+1+(nb_boundary)/2
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
    
