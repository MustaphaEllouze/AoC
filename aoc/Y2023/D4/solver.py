from typing import Any
from aoc.tools import ABCSolver
from collections import defaultdict

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        def number_of_hits(indline:int)->int:
            winning, mynumbers = self.data[indline].split(':')[1].split('|')
            winning = [int(e) for e in winning.split()]
            mynumbers = [int(e) for e in mynumbers.split()]
            hits = sum([int(e in winning) for e in mynumbers])
            return hits

        if not part2 : 
            rpart1 = 0
            for i,card in enumerate(self.data) :
                hits = number_of_hits(i)
                if hits>0 : rpart1 += 2**(hits-1)
            return 'No structure', rpart1
        else:
            rpart2 = 0
            queue = defaultdict(int)
            for i, line in enumerate(self.data) : queue[i]=1

            while len(queue.keys())>0:
                ind = list(queue.keys())[0]
                num = queue.pop(ind)
                # print(f'Card {ind+1} : {num} times')
                hits = number_of_hits(ind)
                for i in range(hits) : 
                    queue[ind+i+1]+=num
                    # print(f'Unlocking card {ind+i+2} : {num} times')
                rpart2 += num
            
            return 'No structure', rpart2
            
    def generate_view(self, structure: Any) -> str:
        return structure