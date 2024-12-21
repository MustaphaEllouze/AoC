from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map
from collections import defaultdict

def find_path(map:Map)->tuple[int, tuple[int, int]]:
    start_pos = map.find('S')
    end_pos = map.find('E')
    to_visit = [(start_pos, 0, (start_pos,))]
    visited = []
    while to_visit:
        pos,time,path = to_visit.pop(0)
        if pos in visited : continue
        visited.append(pos)
        if pos == end_pos :
            return (time,path)
        for neigh in map.cardinal_neighbours(*pos):
            if map(*neigh) in ['.', 'E']:
                to_visit.append((neigh, time+1, (*path, neigh)))

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        map = Map(raw_data=self.data)

        no_cheat_time,best_path = find_path(map)
        found = defaultdict(int)

        for i,pos in enumerate(best_path):
            print(f'{i}/{len(best_path)}', end='\r')
            idx_pos = best_path.index(pos)
            for pos_pos, mid_pos in (
                (map.left(*map.left(*pos)), map.left(*pos)),
                (map.up(*map.up(*pos)), map.up(*pos)),
                (map.right(*map.right(*pos)), map.right(*pos)),
                (map.down(*map.down(*pos)), map.down(*pos)),
            ):
                if pos_pos is None : continue
                if not pos_pos in best_path : continue
                if not map(*mid_pos) == '#' : continue
                idx_pospos = best_path.index(pos_pos)
                if idx_pospos < idx_pos : continue
                found[idx_pospos-idx_pos-2] += 1
        
        print(found)

        return None, sum([v for k,v in found.items() if k>=100])
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)