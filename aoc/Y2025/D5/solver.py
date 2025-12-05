from typing import Any
from aoc.tools import ABCSolver, Map

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        fresh_range = []
        ids = []
        switch = False
        for line in self.data : 
            if line == '' : switch = True
            elif switch : ids.append(int(line))
            else      : fresh_range.append([int(e) for e in line.split('-')])

        if not part2 :
            fresh_id = [
                i 
                for i in ids
                if any([i>=e[0] and i<=e[1] for e in fresh_range])
            ]        

            result = len(fresh_id)
        else :
            bounds = [(e[0], 1) for e in fresh_range] + [(e[1], -1) for e in fresh_range]
            bounds = sorted(bounds, key= lambda x:x[0])
            status = 0
            detected_start = None
            detected_end = None
            new_ranges = []
            for bound, close_value in bounds:
                old_status = status
                status += close_value
                if old_status == 0 and status == 1 : 
                    detected_start = bound
                if status == 0 :
                    detected_end = bound
                    new_ranges.append([detected_start, detected_end])
                    detected_start = None
                    detected_end = None
            result = sum([b-a+1 for a, b in new_ranges])

        return None, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
