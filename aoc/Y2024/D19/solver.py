from typing import Any
from aoc.tools import ABCSolver

from functools import lru_cache

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        towels = self.data[0].split(', ')
        goals = self.data[2:]

        @lru_cache
        def resolver(goal:str)->bool|int:
            if goal == '' : return True
            chck_list = [
                resolver(goal[len(tow):])
                for tow in towels
                if goal.startswith(tow)
            ]
            return any(chck_list) if not part2 else sum(chck_list)

        return None, sum([resolver(g) for g in goals])
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)