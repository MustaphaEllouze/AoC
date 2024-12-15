from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict

from aoc.tools import Map

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        split_lines = []
        split_lines2  =[]
        break_line = False

        for line in self.data :
            if line == '' : break_line = True
            if break_line : split_lines2.append(line)
            else : split_lines.append(line)

        map = Map(raw_data=split_lines)
        commands = list(''.join(split_lines2))

        cur_pos = map.find(value='@')
        directions = {
            'v' : 'D',
            '^' : 'U',
            '>' : 'R',
            '<' : 'L',
        }
        for c in commands:
            closest_dot = map.find_in_direction(
                *cur_pos,
                direction=directions[c],
                value='.'
            )
            closest_wall = map.find_in_direction(
                *cur_pos,
                direction=directions[c],
                value='#'
            )
            if not closest_dot : 
                continue
            if abs(cur_pos[0]-closest_wall[0])+abs(cur_pos[1]-closest_wall[1]) \
                < abs(cur_pos[0]-closest_dot[0])+abs(cur_pos[1]-closest_dot[1]):
                continue
            else:
                to_move = map.list_between_two(
                    *cur_pos,
                    *closest_dot,
                )
                if directions[c] in ['U', 'L'] : 
                    to_move = to_move[::-1]
                symbols = ['.']+[map(*o) for o in to_move][:-1]
                for o,no in zip(to_move, symbols): 
                    map.map[o] = no
                match directions[c]:
                    case 'U': cur_pos = (cur_pos[0]-1, cur_pos[1])
                    case 'D': cur_pos = (cur_pos[0]+1, cur_pos[1])
                    case 'L': cur_pos = (cur_pos[0], cur_pos[1]-1)
                    case 'R': cur_pos = (cur_pos[0], cur_pos[1]+1)
        
        for o in map.findall('O'):
            result += o[0]*100+o[1]

        return map, result
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)