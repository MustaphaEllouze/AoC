from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map
from collections import defaultdict

def find_path(map:Map)->tuple[int, int]:
    start_pos = map.find('S')
    end_pos = map.find('E')
    to_visit = [(start_pos, 0, (start_pos,))]
    visited = []
    while to_visit:
        pos,time,path = to_visit.pop(0)
        if pos in visited : continue
        visited.append(pos)
        if pos == end_pos :
            return path
        for neigh in map.cardinal_neighbours(*pos):
            if map(*neigh) in ['.', 'E']:
                to_visit.append((neigh, time+1, (*path, neigh)))

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        map = Map(raw_data=self.data)

        best_path = find_path(map)
        found = defaultdict(int)

        indexes = {t:i for i,t in enumerate(best_path)}

        proximo = defaultdict(list)
        for i,pos in enumerate(best_path):
            print(f'{i}/{len(best_path)}', end='\r')
            for posi in best_path:
                if 0<abs(pos[0]-posi[0])+abs(pos[1]-posi[1])<=2+18*part2:
                    proximo[pos].append(posi)
        
        for pos,prox in proximo.items():
            for propro in prox:
                time_gained =indexes[propro]-indexes[pos]-abs(pos[0]-propro[0])-abs(pos[1]-propro[1])
                if time_gained>0:
                    found[time_gained] += 1

        return None, sum([v for k,v in found.items() if k>=100])
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)