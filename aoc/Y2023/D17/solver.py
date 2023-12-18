from typing import Any
from aoc.tools import ABCSolver, Map
from bisect import insort
from collections import defaultdict

REVERSED = dict(zip('SDURL', 'SUDLR'))

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([[int(e) for e in list(line)] for line in self.data])

        if not part2 : 
            MAXDIRECTION = 3
            MINDIRECTION = 1
        else:
            MAXDIRECTION = 10
            MINDIRECTION = 4

        # Case, heatloss, nombres cases même direction, même direction, path, subpath
        current = (
            (0,0), # coords
            0,     # heatloss 
            0,     # nombre direction
            'S',   # direction
            'S',   # path
        )
        visited = defaultdict(list)
        to_visit = [current]

        best_path = None

        last_ten = []
        iterator = 0

        while to_visit:
            iterator += 1
            coords, heatloss, nb_direction, direction, path = to_visit.pop(0)
            if path[-MAXDIRECTION:] in visited[coords] : continue
            visited[coords].append(path[-MAXDIRECTION:])
            last_ten.append(coords)
            if len(last_ten)>10 : last_ten.pop(0)
            if iterator % 10000 == 0 : 
                print(sum([c[0] for c in last_ten])/10, sum([c[1] for c in last_ten])/10)
            # print(coords, len(to_visit))
            if coords == (map.height-1, map.width-1):
                if all([e==path[-1] for e in path[-MINDIRECTION:]]) :
                    best_path = heatloss
                    print(path)
                    break
                else : continue
            for nei,dir_nei in [
                (map.up(    *coords),'U'), 
                (map.down(  *coords),'D'), 
                (map.right( *coords),'R'), 
                (map.left(  *coords),'L'),
            ]:
                if nei \
                and dir_nei != REVERSED[direction]\
                and ( 
                    (nb_direction<MINDIRECTION and (dir_nei == direction or direction == 'S'))
                    or 
                    (MINDIRECTION<=nb_direction<MAXDIRECTION)
                    or 
                    (nb_direction==MAXDIRECTION and dir_nei!=direction)
                ):
                
                    insort(
                        to_visit,
                        (
                            nei,
                            heatloss+map(*nei),
                            nb_direction*(dir_nei==direction)+1,
                            dir_nei,    
                            path+dir_nei,
                        ),
                        key = lambda x: x[1],
                    )
        return map.map, best_path
    
    def generate_view(self, structure: Any) -> str:
        result = '\n'
        result += "\n".join(
            "".join(str(e) for e in line)
            for line in structure
        )
        return result