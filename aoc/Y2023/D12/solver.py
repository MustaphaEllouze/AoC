from typing import Any
from aoc.tools import ABCSolver, jokerize

class LineProblem :

    def __init__(self, problem:str, hints:list[int]) -> None:
        self.problem = problem
        self.hints = hints
        self.remaining_indices = [[h,True] for h in self.hints]
    
    def __str__(self)->str:
        return f'{self.problem} || hints : {self.hints}'
    
    def is_ok(self)->bool:
        return all([e in ['.','#'] for e in self.problem]) \
            and all([len(e)==h for e,h in zip([e for e in self.problem.split('.') if e != ''], self.hints)])
    
    def solve_bruteforce(self)->list[str]:
        arrangements = [e for e in jokerize(self.problem, '?', ['.','#'])]
        possibilities = []
        for arr in arrangements :
            splitter = [e for e in arr.split('.') if e != '']
            if len(splitter)==len(self.hints) : 
                if all([len(e)==h for e,h in zip(splitter, self.hints)]):
                    possibilities.append(splitter)
        return possibilities
    
    # def solve_smart_old(self)->list[str]:

    #     # Ensemble des indice que j'ai 
    #     treat_hints = sorted(self.hints)

    #     # Ce que je sais au début
    #     what_i_know = self.problem

    #     # Il faut commencer ici
    #     treat_those = [('', what_i_know, [h for h in treat_hints])]
        
    #     # On fera le check réel sur ces strings
    #     final_check_those = []

    #     while len(treat_those)>0:

    #         # On récupère ce qu'on sait
    #         previous, current_know, current_hints = treat_those.pop()
    #         # S'il n'y a plus d'indice, on enregistre et on passe 
    #         if len(current_hints) == 0 : 
    #             final_check_those.append(previous.replace('?','.').replace('X','#'))
    #             continue

    #         else:
    #             # On récupère l'indice d'après
    #             next_hint = current_hints[0]
                
    #             # Pour chaque bout qui pourrais être remplacé
    #             for i in range(0, len(current_know)-next_hint+1):
    #                 if all([e in ['?', '#'] for e in current_know[i:i+next_hint]]):
                        
    #                     # On l'ajoute en tant que truc à traiter
    #                     treat_those.append(
    #                         (
    #                             previous+current_know[:i]+('X'*next_hint),
    #                             current_know[i+next_hint:],
    #                             current_hints[1:]
    #                         )
    #                     )
    #     result = [c for c in final_check_those if LineProblem(c, self.hints).is_ok()]
    #     print(result)
    #     return result

    def assess_known(self)->None:
        pass

    def solve_smart(self, )->list[str]:
        pass


class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        problems = [
            LineProblem(
                problem=line.split()[0],
                hints = [int(e) for e in line.split()[1].split(',')]
            )
            for line in self.data
        ]

        result = 0
        for i,p in enumerate(problems):
            result += len(p.solve_bruteforce())
            p.solve_smart()
            print(i/len(problems))


        return 'No structure', result
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)