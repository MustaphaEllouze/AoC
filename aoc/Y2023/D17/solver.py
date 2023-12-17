from typing import Any
from aoc.tools import ABCSolver, Map
from bisect import insort
from collections import defaultdict

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([[int(e) for e in list(line)] for line in self.data])

        # Case, heatloss, nombres cases même direction, même direction, path, subpath
        current = ((0,0),0,0, 'S','S')
        visited = defaultdict(list)
        to_visit = [current]

        best_path = None

        while to_visit:
            coords, heatloss, nb_direction, direction, path = to_visit.pop(0)
            if path[-3:] in visited[coords] : continue
            visited[coords].append(path[-3:])
            print(coords, len(to_visit))
            if coords == (map.height-1, map.width-1) : 
                best_path = heatloss
                print(path)
                break
            for nei,dir_nei in [
                (map.up(    *coords),'U'), 
                (map.down(  *coords),'D'), 
                (map.right( *coords),'R'), 
                (map.left(  *coords),'L'),
            ]:
                if nei and (dir_nei!=direction or nb_direction<3)\
                and not((dir_nei in 'DU' and direction in 'DU' and dir_nei!=direction))\
                and not((dir_nei in 'LR' and direction in 'lR' and dir_nei!=direction)):
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
        for line in structure:
            for e in line : result += str(e)
            result+='\n'
        return result