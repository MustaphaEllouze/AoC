from typing import Any
from aoc.tools import ABCSolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
import os

from aoc.tools.map import Map

def does_it_finish(map_init:Map, pos_line_obs:int, pos_col_obs:int)->tuple[Map,int,bool]:

    map = deepcopy(map_init)

    pos_line, pos_col = map.find(value='^')
    direction = 'U'

    if pos_line_obs and pos_col_obs : 
        map.map[pos_line_obs, pos_col_obs] = '#'

    been_there_done_that = []

    while True:
        map.map[pos_line, pos_col] = 'X'
        if (pos_line, pos_col, direction) in been_there_done_that :
            return None, None, False
        else:
            been_there_done_that.append((pos_line, pos_col,direction))
        match direction:
            case 'U':
                next_pos = map.up(pos_line, pos_col)
                if not next_pos : 
                    break
                elif map(*next_pos) == '#':
                    direction = 'R'
                else:
                    pos_line, pos_col = next_pos
            
            case 'R':
                next_pos = map.right(pos_line, pos_col)
                if not next_pos : 
                    break
                elif map(*next_pos) == '#':
                    direction = 'D'
                else:
                    pos_line, pos_col = next_pos
            
            case 'D':
                next_pos = map.down(pos_line, pos_col)
                if not next_pos : 
                    break
                elif map(*next_pos) == '#':
                    direction = 'L'
                else:
                    pos_line, pos_col = next_pos
            
            case 'L':
                next_pos = map.left(pos_line, pos_col)
                if not next_pos : 
                    break
                elif map(*next_pos) == '#':
                    direction = 'U'
                else:
                    pos_line, pos_col = next_pos
    
    return map.map, len(map.findall(value='X')), True

def check_dot(map:Map, dot:tuple[int, int]):
    copy_map = deepcopy(map)
    copy_map.map[*dot] = '#'
    return does_it_finish(
        map_init=copy_map, 
        pos_line_obs=dot[0],
        pos_col_obs=dot[1],
        )[2]

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        map = Map([list(line) for line in self.data])

        if not part2 :

            return does_it_finish(
                map_init = map,
                pos_line_obs=None,
                pos_col_obs=None,
            )[0:2]

        if part2 :
            
            all_dots = map.findall(value='.')

            result = 0

            def process_dot(dot):
                is_loop = not check_dot(map, dot)
                if is_loop : print(f"Loop found: {dot}")
                return is_loop

            with ThreadPoolExecutor() as executor:
                futures = []
                for dot in all_dots:
                    future = executor.submit(process_dot, dot)
                    futures.append(future)

                for i,future in enumerate(as_completed(futures)):
                    print(f'{i}/{len(all_dots)}', end='\r')
                    result += int(future.result())
                
            return None, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)