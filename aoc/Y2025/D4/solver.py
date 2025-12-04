from typing import Any
from aoc.tools import ABCSolver, Map

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        result = 0

        map = Map(raw_data=self.data)

        if not part2 :
            for coords in map.iterator :
                if map(*coords) == '@' \
                    and sum(
                        [
                            map(*c) == '@' 
                            for c in map.neighbours(*coords)
                        ]
                    )<4: 
                    result += 1

        else :
            remove_this = [True]
            while(remove_this):
                remove_this = []
                for coords in map.iterator :
                    if map(*coords) == '@' \
                        and sum(
                            [
                                map(*c) == '@' 
                                for c in map.neighbours(*coords)
                            ]
                        )<4: 
                        remove_this.append(coords)
                result += len(remove_this)
                for coords in remove_this :
                    map.map[*coords] = '.'

        return map, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
