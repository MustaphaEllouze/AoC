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
            print(len(to_visit), abs(pos[0]-goal[0])+abs(pos[1]-goal[1]))
            pos, direc, score, dico = to_visit.pop(0)
            if pos in visited : 
                continue
            visited.append(pos)

            up = map.up(*pos)
            down = map.down(*pos)
            right = map.right(*pos)
            left = map.left(*pos)

            for n,d in zip([up, down, right, left], ['U', 'D', 'R', 'L']):
                if n:
                    if map(*n) in ['.', 'E']:
                        insort(
                            to_visit, 
                            (
                                n, 
                                d, 
                                score+1+1000*(d!=direc), 
                                {**dico, **{n:score+1+1000*(d!=direc)}}
                            ),
                            key=lambda x:x[2]
                        )

        best_dico = dico
        best_score = score

        if not part2 : return map, best_score

        # Search all paths that lead to E
        pos = map.find(value='S')
        goal = map.find(value='E')

        to_visit = [(pos, 'R', 0, {pos:0})]
        # goal_found = []
        visited = []
        while to_visit:
            print('PART2', len(to_visit), abs(pos[0]-goal[0])+abs(pos[1]-goal[1]))
            pos, direc, score, dico = to_visit.pop(0)
            if score > best_score : break
            if (pos,direc) in visited :
                if pos in best_dico and best_dico[pos] == dico[pos]:
                    best_dico.update(dico)
                continue
            visited.append((pos, direc))

            up = map.up(*pos)
            down = map.down(*pos)
            right = map.right(*pos)
            left = map.left(*pos)

            for n,d in zip([up, down, right, left], ['U', 'D', 'R', 'L']):
                if direc == 'U' and d == 'D' : continue
                if direc == 'D' and d == 'U' : continue
                if direc == 'R' and d == 'L' : continue
                if direc == 'L' and d == 'R' : continue
                if n:
                    if map(*n) in ['.', 'E']:
                        insort(
                            to_visit, 
                            (
                                n, 
                                d, 
                                score+1+1000*(d!=direc), 
                                {**dico, **{n:score+1+1000*(d!=direc)}}
                            ),
                            key=lambda x:x[2]
                        )
        
        # print(len(goal_found))

        for pos in best_dico:
            map.map[*pos] = 'O'
        
        # print(sorted(best_dico.items(), key=lambda x:x[1]))

        return map, len(best_dico)
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)