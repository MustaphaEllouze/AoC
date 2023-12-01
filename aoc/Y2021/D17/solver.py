from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        tx, ty = self.data[0].split(':')[1].split(',')
        y0, y1 = ty.split('=')[1].split('..')
        y0, y1 = int(y0), int(y1)

        x0, x1 = tx.split('=')[1].split('..')
        x0, x1 = int(x0), int(x1)

        # en y 
        best_velocity = y0-1
        candidates = []
        steps = []

        while best_velocity<=100 :
            best_velocity += 1
            maximum_height = best_velocity*(best_velocity+1)/2
            init_step = 0
            current_height = maximum_height
            while current_height>y0 :
                init_step += 1
                current_height -= init_step
                if current_height<=y1 and current_height>=y0: 
                    candidates.append(best_velocity)
                    steps.append(best_velocity+init_step)
        
        # en x 
        cross_candidates = []
        
        for candidate, step in zip(candidates, steps):
            print(candidate, step)
            for velocity_x in range(1, x1+1):
                targetx = sum([max(0, velocity_x-i) for i in range(0, step+1)])
                if x0<=targetx<=x1 : cross_candidates.append((velocity_x, candidate))

        cross_candidates = list(set(cross_candidates))
        for c in cross_candidates : print(c)

        if not part2 : 
            return 'No structure', max(candidates)*(max(candidates)+1)/2
        else:
            return 'No structure', len(cross_candidates)
    
    def generate_view(self, structure: Any) -> str:
        return 'No view'