from typing import Any
from aoc.tools import ABCSolver
from collections import defaultdict
import copy

NSTEP=40

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        polymer = self.data[0]

        rules = {
            line.split('->')[0].strip() : line.split('->')[1].strip()
            for line in self.data[2:]
        }

        if not part2 : 
            polymers = [polymer]

            step_polymer = polymer

            for step in range(NSTEP):
                print(f'Step {step}')
                new_polymer = ''
                for a,b in zip(step_polymer[:-1], step_polymer[1:]):
                    new_polymer+= a + rules[a+b]
                step_polymer = new_polymer

                step_polymer+=b
                polymers.append(step_polymer)

            countletters = defaultdict(int)
            for let in polymers[-1] : countletters[let]+=1
            return polymers, max(countletters.values())-min(countletters.values())

        else : 
            successions = defaultdict(int)
            for a,b in zip(polymer[:-1], polymer[1:]):
                successions[a+b]+=1
            smart_rules = {
                pair:[pair[0]+letter, letter+pair[1]]
                for pair,letter in rules.items()
            }

            step_succession = successions
            for step in range(NSTEP):
                new_succession = defaultdict(int)
                for succ, number in step_succession.items() :
                    (p1, p2) = smart_rules[succ]
                    new_succession[p1] += number
                    new_succession[p2] += number
                step_succession = new_succession
            
            letters = defaultdict(int)
            for pair, number in step_succession.items():
                letters[pair[0]] += number

            solution = max(letters.values())-min(letters.values())+1

            return [str((pair, number)) for pair,number in step_succession.items()], solution

    
    def generate_view(self, structure: Any) -> str:
        result = ''
        for poly in structure:
            result += '\n' + poly
        return result