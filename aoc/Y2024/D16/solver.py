from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map
from bisect import insort

clockwise = {
    'R' : 'D',
    'D' : 'L',
    'L' : 'U',
    'U' : 'R',
}
trigowise = {
    'R' : 'U',
    'U' : 'L',
    'L' : 'D',
    'D' : 'R',
}

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        map = Map(raw_data=self.data)

        pos = map.find(value='S')
        goal = map.find(value='E')

        to_visit = [(pos, 'R', 0, {pos:0})]
        visited = []

        while to_visit and pos != goal:
            # print(len(to_visit), abs(pos[0]-goal[0])+abs(pos[1]-goal[1]))
            pos, direc, score, dico = to_visit.pop(0)
            if (pos,direc) in visited : 
                continue
            visited.append((pos, direc))

            insort(to_visit, (pos, clockwise[direc], score+1000, {**dico, **{pos:score+1000}}), key=lambda x:x[2])
            insort(to_visit, (pos, trigowise[direc], score+1000, {**dico, **{pos:score+1000}}), key=lambda x:x[2])

            match direc:
                case 'U':
                    if map(*map.up(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.up(*pos), direc, score+1, {**dico, **{map.up(*pos):score+1}}), key=lambda x:x[2])
                case 'D':
                    if map(*map.down(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.down(*pos), direc, score+1, {**dico, **{map.down(*pos):score+1}}), key=lambda x:x[2])
                case 'R':
                    if map(*map.right(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.right(*pos), direc, score+1, {**dico, **{map.right(*pos):score+1}}), key=lambda x:x[2])
                case 'L':
                    if map(*map.left(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.left(*pos), direc, score+1, {**dico, **{map.left(*pos):score+1}}), key=lambda x:x[2])

        best_dico = dico
        best_score = score

        if not part2 : return map, best_score

        pos = map.find(value='S')
        goal = map.find(value='E')

        to_visit = [(pos, 'R', 0, {pos:0})]
        visited = []

        while to_visit and pos != goal:
            # print(len(to_visit), abs(pos[0]-goal[0])+abs(pos[1]-goal[1]))
            pos, direc, score, dico = to_visit.pop(0)
            if pos in best_dico :
                if best_dico[pos] == dico[pos] :
                    print('upgrade', pos)
                    best_dico = {**best_dico, **dico}
            if (pos,direc) in visited : 
                continue
            visited.append((pos, direc))

            insort(to_visit, (pos, clockwise[direc], score+1000, {**dico, **{pos:score+1000}}), key=lambda x:x[2])
            insort(to_visit, (pos, trigowise[direc], score+1000, {**dico, **{pos:score+1000}}), key=lambda x:x[2])

            match direc:
                case 'U':
                    if map(*map.up(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.up(*pos), direc, score+1, {**dico, **{map.up(*pos):score+1}}), key=lambda x:x[2])
                case 'D':
                    if map(*map.down(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.down(*pos), direc, score+1, {**dico, **{map.down(*pos):score+1}}), key=lambda x:x[2])
                case 'R':
                    if map(*map.right(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.right(*pos), direc, score+1, {**dico, **{map.right(*pos):score+1}}), key=lambda x:x[2])
                case 'L':
                    if map(*map.left(*pos)) in ['.', 'E']:
                        insort(to_visit, (map.left(*pos), direc, score+1, {**dico, **{map.left(*pos):score+1}}), key=lambda x:x[2])

        for pos in best_dico:
            map.map[*pos] = 'O'
        
        # print(sorted(best_dico.items(), key=lambda x:x[1]))

        return map, len(best_dico)
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)