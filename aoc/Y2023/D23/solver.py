from typing import Any
from aoc.tools import Map, ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([list(line) for line in self.data])
        starting_point = (0,1)
        finish_point = (map.height-1, map.width-2)
        
        assert map(*finish_point) == '.'

        # current_point, step_taken, #visited
        path = [(starting_point,0, [starting_point])]
        finished_path = []

        while any([e[0]!=finish_point for e in path]):
            print('Computing',len(path),'paths in total. Finished', len(finished_path), 'paths already.')
            new_iteration_path = []
            for i,p in enumerate(path) :
                c,step,the_path = p
                if map(*c) == '>' and not part2: 
                    neighs = [e for e in [map.right(*c)] if e is not None]
                elif map(*c) == '<' and not part2: 
                    neighs = [e for e in [map.left(*c)] if e is not None]
                elif map(*c) == '^' and not part2: 
                    neighs = [e for e in [map.up(*c)] if e is not None]
                elif map(*c) == 'v' and not part2: 
                    neighs = [e for e in [map.down(*c)] if e is not None]
                else : # map(*c) == '.' 
                    neighs = map.cardinal_neighbours(*c)
                admissible = [n for n in neighs if map(*n)!='#' and n not in the_path]
                for a in admissible :
                    if a != finish_point : 
                        new_iteration_path.append((a, step+1, the_path+[a]))
                    else : 
                        finished_path.append((a, step+1, the_path+[a]))
            path = new_iteration_path
        
        return 'No structure', max([fp[1] for fp in finished_path])
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)