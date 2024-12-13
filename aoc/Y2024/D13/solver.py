from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict

import re

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0
        buttonA = re.compile(r"Button A: X\+(\d*), Y\+(\d*)")
        buttonB = re.compile(r"Button B: X\+(\d*), Y\+(\d*)")
        prize = re.compile(r"Prize: X=(\d*), Y=(\d*)")

        for l1, l2, l3 in zip(
            self.data[0::4],
            self.data[1::4],
            self.data[2::4],
        ):
            xa, ya = [int(e) for e in re.match(buttonA, l1).groups()]
            xb, yb = [int(e) for e in re.match(buttonB, l2).groups()]
            xp, yp = [int(e) for e in re.match(prize, l3).groups()]

            if part2 :
                xp += 10000000000000
                yp += 10000000000000

            # A*xa + B*xb = xp
            # A*ya + B*yb = yp
            # A<=100 ; B<=100

            # C'est un système d'équations à deux inconnues avec second membre

            # Si le déterminant est nul, pas de solution:
            if xa*yb == ya*xb : continue

            # Sinon, on résoud
            deter = xa*yb - ya*xb

            A = (xp*yb - yp*xb)/deter
            B = (xa*yp - ya*xp)/deter

            # On vérifie que ce sont des valeurs entières
            if int(A) != A or int(B) != B : continue

            # On vérifie qu'elles sont plus petites que 100
            if not part2 and (A>100 or B>100) : continue

            # On vérifie qu'on est positifs quand même:
            if A<0 or B<0 : continue

            # Sinon on ajoute
            result += int(3*A + B)

        return None, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)