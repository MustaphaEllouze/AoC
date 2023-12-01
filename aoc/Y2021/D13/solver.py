from typing import Any
from aoc.tools import ABCSolver, Map
import copy

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
        
        flag_folds = False
        folds = []
        dots = []

        feuilles = []

        for line in self.data : 
            if line == '' : 
                flag_folds = True
                continue
            if not flag_folds : 
                dots.append(tuple(line.split(',')))
            else :
                folds.append(tuple(line.strip('fold along ').split('=')))
        
        
        xs = [int(p[0]) for p in dots]
        ys = [int(p[1]) for p in dots]

        feuille = Map([[0]*(max(xs)+1)]*(max(ys)+1))

        for x,y in zip(xs, ys):
            feuille.map[y, x] = 1
        
        feuilles.append(copy.copy(feuille.map))

        def fold_x(f:Map, x:int):
            new_f = Map([[0]*x]*(f.height))
            for element in new_f.iterator:
                new_f.map[*element] = max(
                    f.map[*element],
                    f.map[element[0], f.width-element[1]-1],
                )
            
            return new_f

        def fold_y(f:Map, y:int):
            new_f = Map([[0]*f.width]*y)
            for element in new_f.iterator:
                new_f.map[*element] = max(
                    f.map[*element],
                    f.map[f.height-element[0]-1, element[1]],
                )
            
            return new_f

        for direction, line in folds :
            if direction == 'x' : func = fold_x
            if direction == 'y' : func = fold_y

            feuille = func(feuille, int(line))

            feuilles.append(copy.copy(feuille.map))

            if not part2:
                return feuilles, sum(sum(feuille.map))

        result = '\n'
        for line in feuille.map : 
            for carac in line :
                result += '#' if carac == 1 else ' '
            result += '\n'

        return feuilles, result
    
    def generate_view(self, structure: Any) -> str:
        result = '\n'
        for feuille in structure : result+=str(feuille)+'\n'
        return result[:-1]