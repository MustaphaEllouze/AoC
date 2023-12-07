from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
        
        thedict = {
            1: [False, {}, "seed-to-soil"],
            2: [False, {}, "soil"],
            3: [False, {}, "fertilizer"],
            4: [False, {}, "water"],
            5: [False, {}, "light"],
            6: [False, {}, "temperature"],
            7: [False, {}, "humidity"],
        }

        step = 1
        seedspart2 = []
        for line in self.data:
            if "seeds" in line:
                seeds = [int(e) for e in line.split(":")[1].split()]
                seedspart2 = [(e, e + d - 1) for (e, d) in zip(seeds[::2], seeds[1::2])]
            if thedict[step][0] and line != "":
                arr, dep, numb = line.split()
                thedict[step][1][(int(dep), int(dep) + int(numb) - 1)] = int(arr) - int(dep)
            elif thedict[step][0] and line == "":
                thedict[step][0] = False
                step += 1
            elif line.startswith(thedict[step][2]):
                thedict[step][0] = True


        def getnew(adict, number):
            for (mini, maxi), decalage in adict.items():
                if mini <= number <= maxi:
                    return int(number) + decalage
            return number


        def get_location(seed: int):
            s0 = int(seed)
            s1 = getnew(thedict[1][1], s0)
            s2 = getnew(thedict[2][1], s1)
            s3 = getnew(thedict[3][1], s2)
            s4 = getnew(thedict[4][1], s3)
            s5 = getnew(thedict[5][1], s4)
            s6 = getnew(thedict[6][1], s5)
            s7 = getnew(thedict[7][1], s6)
            return s7


        def reverse_dict(adict: dict):
            return {
                (getnew(adict, dep), getnew(adict, maxdep)): -dec
                for (dep, maxdep), dec in adict.items()
            }


        reversed_dicts = {i: reverse_dict(thedict[i][1]) for i in range(1, 8)}


        def get_seed(location: int):
            l0 = int(location)
            l1 = getnew(reversed_dicts[7], l0)
            l2 = getnew(reversed_dicts[6], l1)
            l3 = getnew(reversed_dicts[5], l2)
            l4 = getnew(reversed_dicts[4], l3)
            l5 = getnew(reversed_dicts[3], l4)
            l6 = getnew(reversed_dicts[2], l5)
            l7 = getnew(reversed_dicts[1], l6)
            return l7


        locations = [get_location(s) for s in seeds]

        if not part2 : return 'No structure', min(locations)
        else:
            result = 0
            found = False
            print("Computing solution for part2, this may take some time")
            while not found:
                image = get_seed(location=result)
                for mini, maxi in seedspart2:
                    if mini <= image <= maxi:
                        return 'No structure', result
                result += 1

    def generate_view(self, structure: Any) -> str:
        return 'No view'