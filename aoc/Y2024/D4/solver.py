from typing import Any
from aoc.tools import ABCSolver

from aoc.tools import Map

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        next_letter = {'X':'M', 'M':'A', 'A':'S'}

        map = Map(self.data_map_ready)

        if not part2 :

            x_positions = map.findall(value='X')

            search_buffer : list[tuple[tuple[int, int], str|None, str]] = [
                (x, None, 'X')
                for x in x_positions
            ]

            while search_buffer:
                index, direction, letter = search_buffer.pop()
                
                if letter == 'S' : 
                    result += 1
                    continue

                potential_added_search = []

                if direction == 'U' or not direction:
                    potential_added_search.append((map.up(*index),'U', next_letter[letter]))
                if direction == 'D' or not direction:
                    potential_added_search.append((map.down(*index),'D', next_letter[letter]))
                if direction == 'R' or not direction:
                    potential_added_search.append((map.right(*index),'R', next_letter[letter]))
                if direction == 'L' or not direction:
                    potential_added_search.append((map.left(*index),'L', next_letter[letter]))
                if direction == 'UR' or not direction:
                    potential_added_search.append((map.upright(*index),'UR', next_letter[letter]))
                if direction == 'UL' or not direction:
                    potential_added_search.append((map.upleft(*index),'UL', next_letter[letter]))
                if direction == 'DR' or not direction:
                    potential_added_search.append((map.downright(*index),'DR', next_letter[letter]))
                if direction == 'DL' or not direction:
                    potential_added_search.append((map.downleft(*index),'DL', next_letter[letter]))
                
                while potential_added_search :
                    pot, d, let = potential_added_search.pop()
                    if pot and map(*pot) == let : search_buffer.append((pot, d, let))
        
        if part2 :
            a_positions = map.findall(value='A')

            for index in a_positions :
                ur = map.upright(*index)
                dr = map.downright(*index)
                ul = map.upleft(*index)
                dl = map.downleft(*index)

                if not (ur and dr and ul and dl) : continue

                if (
                    (
                        map(*ur) == 'M' and map(*dl) == 'S'
                    )
                    or (
                        map(*ur) == 'S' and map(*dl) == 'M'
                    )
                ) and (
                    (
                        map(*dr) == 'M' and map(*ul) == 'S'
                    )
                    or (
                        map(*dr) == 'S' and map(*ul) == 'M'
                    )
                ):
                    result += 1

        return map.map, result

    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)