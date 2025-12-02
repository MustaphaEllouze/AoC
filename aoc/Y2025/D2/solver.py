from typing import Any
from aoc.tools import ABCSolver

def solve_with_n(mini:str, maxi:str, N:int)->list[int]:
    hits = []
    if len(mini) % N != 0 :
        mini = 10**(len(mini)-1+N-(len(mini) % N))
    if len(maxi) % N != 0 :
        maxi = 10**(len(maxi)-(len(maxi) % N))-1
    mini = int(mini)
    maxi = int(maxi)
    if mini > maxi : return hits
    split_mini = int(str(mini)[:len(str(mini))//N])
    split_maxi = int(str(maxi)[:len(str(maxi))//N])
    for tobetested in range(split_mini, split_maxi+1):
        colle = int(str(tobetested)*N)
        if mini <= colle <= maxi :
            hits.append(colle)
    return hits

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:


        data = [
             couple.split('-')
             for couple in self.data[0].split(',')
        ]

        result = 0

        if not part2 :
            for mini, maxi in data :
                result += sum(solve_with_n(mini, maxi, 2))
        else :
            for mini, maxi in data :
                sub_result = []
                for i in range(2, len(maxi)+1):
                    sub_result += solve_with_n(mini, maxi, i)
                result += sum(set(sub_result))

        return None, result

    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)
