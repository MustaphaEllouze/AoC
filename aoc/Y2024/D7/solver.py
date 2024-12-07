from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        view = []

        for line in self.data:
            target, numbers = line.split(':')
            numbers = [int(e) for e in numbers.strip().split()]
            target = int(target)

            have_to_check_those = [(target, numbers, '')]

            while have_to_check_those:
                target_rest, rest, curr_operation = have_to_check_those.pop()
                view.append(f'{target_rest}, {rest}, {curr_operation}')
                if len(rest)==1 and rest[0]!=target_rest : continue
                if target_rest == 1 and not rest: 
                    curr_operation = curr_operation[2:]
                    curr_operation = '('*(len(numbers)-1) + curr_operation
                    view.append(f'----------, {target}, {numbers}, IS OK with this operation: {curr_operation}')
                    result += target
                    break
                if not rest or target_rest<=0:
                    continue
                if target_rest%rest[-1] == 0 :
                    have_to_check_those.append((target_rest//rest[-1], rest[:-1], f')*{rest[-1]}{curr_operation}'))
                have_to_check_those.append((target_rest-rest[-1], rest[:-1], f')+{rest[-1]}{curr_operation}'))
                if len(rest)>1 and part2:
                    new_target_rest = str(target_rest)[:-len(str(rest[-1]))]
                    deleted_target = str(target_rest)[-len(str(rest[-1])):]
                    if not new_target_rest : continue
                    if not int(deleted_target) == rest[-1] : continue
                    have_to_check_those.append((int(new_target_rest), rest[:-1], f')||{rest[-1]}{curr_operation}'))

        
                
        return "\n".join(view), result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)