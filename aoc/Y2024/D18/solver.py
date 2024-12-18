from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        if self.dataname == '.example' : 
            MAX_DISTANCE = 7
            simu_time = 12
        elif self.dataname == '.input' :
            MAX_DISTANCE = 71
            simu_time = 1024
        else:
            raise NotImplementedError()
        
        start_pos = (0,0)
        goal = (MAX_DISTANCE-1, MAX_DISTANCE-1)

        map = Map([['.']*MAX_DISTANCE]*MAX_DISTANCE)

        for i,line in enumerate(self.data):
            if i == simu_time : break
            y,x = line.split(',')
            x,y = int(x),int(y)
            map.map[x, y] = '#'
        
        if not part2:
            to_visit = [(start_pos, 0)]
            visited = []

            while to_visit:
                pos, steps = to_visit.pop(0)
                if pos == goal : break
                if pos in visited : continue
                visited.append(pos)
                for neigh in map.cardinal_neighbours(*pos):
                    if neigh and map(*neigh) == '.':
                        to_visit.append((neigh, steps+1))

            return map, steps
        else:
            still_possible = True
            offset = 0
            last_best_path = ()

            while still_possible:
                offset += 1 
                y,x = self.data[simu_time+offset].split(',')
                x,y = int(x),int(y)
                map.map[x, y] = '#'
                if last_best_path and (x,y) not in last_best_path : continue
                
                to_visit = [(start_pos, 0, (start_pos,))]
                visited = []
                while to_visit:
                    pos, steps, path = to_visit.pop(0)
                    if pos == goal : 
                        last_best_path = path
                        break
                    if pos in visited : continue
                    visited.append(pos)
                    for neigh in map.cardinal_neighbours(*pos):
                        if neigh and map(*neigh) == '.':
                            to_visit.append((neigh, steps+1, (*path, neigh)))
                if not to_visit and pos != goal : still_possible = False
            
            return map, f'{y},{x}'
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)