from typing import Any
from aoc.tools import ABCSolver

from functools import cache

class LineProblem:
    def __init__(self, problem:str, hints:list[int]):
        self.problem = problem
        self.hints = hints

    def __str__(self)->str:
        return f'{self.problem} || hints : {self.hints}'

@cache
def solve_smart(problem:str, hints:list[int])->int:
    if len(problem)==0 : return 0
    if sum(hints)+len(hints)-1>len(problem) : return 0
    if len(hints)==1:
        result = 0
        for i in range(0, len(problem)-hints[0]+1):
            if not '.' in problem[i: i+hints[0]]\
            and not '#' in problem[:i]\
            and not '#' in problem[i+hints[0]:]:
                result += 1
        return result
    else:
        result = 0
        updatedhints = [e for e in hints]
        updated_problem = problem[1:]
        if problem[0] == '#' :
            updatedhints[0] -= 1
            if updatedhints[0]==0 :
                updatedhints.pop(0)
                updated_problem = updated_problem[1:]
        if problem[hints[0]]!='#':
            subpb1 = LineProblem(problem[hints[0]+1:], hints[1:])
            subpb2 = LineProblem(problem[:hints[0]], [hints[0]])
            sol1 = solve_smart(subpb1.problem, tuple(subpb1.hints))
            sol2 = solve_smart(subpb2.problem, tuple(subpb2.hints))
            result += sol1*sol2
        if problem[0]!='#' :
            subpb3 = LineProblem(updated_problem, updatedhints)
            sol3= solve_smart(subpb3.problem, tuple(subpb3.hints))
            result += sol3
        return result

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        if not part2 : 
            problems = [
                LineProblem(
                    problem=line.split()[0],
                    hints = [int(e) for e in line.split()[1].split(',')]
                )
                for line in self.data
            ]
        else:
            problems = [
                LineProblem(
                    problem=line.split()[0]+('?'+line.split()[0])*4,
                    hints = [int(e) for e in line.split()[1].split(',')]*5
                )
                for line in self.data
            ]

        return 'No structure', sum([solve_smart(p.problem, tuple(p.hints)) for p in problems])
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)