from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict
from itertools import pairwise
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        secret_numbers = defaultdict(list)

        for i,secret in enumerate(self.data):
            print(f'{i}/{len(self.data)}', end='\r')
            res_secret = int(secret)
            secret_numbers[i].append(res_secret)
            for _ in range(2000):
                res_secret_to_mix = res_secret*64
                res_secret = res_secret ^ res_secret_to_mix
                res_secret = res_secret%16777216
                
                res_secret_to_mix = res_secret//32
                res_secret = res_secret ^ res_secret_to_mix
                res_secret = res_secret%16777216
                
                res_secret_to_mix = res_secret*2048
                res_secret = res_secret ^ res_secret_to_mix
                res_secret = res_secret%16777216

                secret_numbers[i].append(res_secret)
            # print(res_secret)
            # print(res_secret)
            result += res_secret
        
        if not part2 :
            return None, result

        secret_changes = {
            k:[None]+[
                e2%10-e1%10 for e1,e2 in pairwise(v)
            ]
            for k,v in secret_numbers.items()
        }

        best_comb = None

        computer : dict[tuple[int, int, int, int], dict[int, int]]= defaultdict(lambda : defaultdict(int))
        for index, changes in secret_changes.items():
            for ch1,ch2,ch3,ch4,s in zip(changes[0:-3], changes[1:-2], changes[2:-1], changes[3:], secret_numbers[index][3:]):
                if computer[(ch1, ch2, ch3, ch4)][index] == 0:
                    computer[(ch1, ch2, ch3, ch4)][index] = s%10
        best_comb = max(computer.keys(), key=lambda x: sum(computer[x].values()))
        best_value = sum(computer[best_comb].values())

        return best_comb, best_value
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)