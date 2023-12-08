from typing import Any
from aoc.tools import ABCSolver
from math import floor

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
        times = [int(e) for e in self.data[0].split(':')[1].split()]
        records = [int(e) for e in self.data[1].split(':')[1].split()]

        def solveeq(tmax:int, threshold:int)->int:
            # Le bâteau se meut à (choose)mm/ms sur une période de (tmax-choose)
            # On résout donc (tmax-x)*x > threshold ie :
            #   x**2 -x*tmax + threshold < 0
            delta = tmax**2 - 4*threshold
            x1 = (tmax-delta**0.5)/2
            x2 =  (tmax+delta**0.5)/2
            result = 0
            if floor(x1)==x1 : result -= 1
            if floor(x2)==x2 : result -= 1
            result += int(x2)-int(x1)
            return result

        if not part2 : 
            respart1 = 1
            for t, r in zip(times, records):
                respart1 *= solveeq(t, r)

            return (times, records), respart1
        else:
            time = ''
            for t in times : time += str(t)
            time = int(time)
            record = ''
            for r in records : record += str(r)
            record = int(record)
            return (time, record), solveeq(time, record)
    
    def generate_view(self, structure: Any) -> str:
        return structure
    