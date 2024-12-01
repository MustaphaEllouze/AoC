import importlib
from aoc.tools import ABCSolver

def main(
    year:int,
    day:int, 
    other_file:str=None, 
    view:bool=False, 
    part2:bool=False,
)->None:
    path_to_solver = f'aoc.Y{year}.D{day}.solver'
    try: 
        solver_file=importlib.import_module(name=path_to_solver)
        solver_class=solver_file.Solver
    except Exception as e:
        print(f'No valid solver found: YEAR={year}; DAY={day}')
        raise e
    
    input_name = 'input' if not other_file else other_file

    solver:ABCSolver=solver_class(
        folder=f'./aoc/Y{year}/D{day}',
        input_file=f'.{input_name}',
    )

    structure, solution=solver.export_result(part2=part2)
    
    prefix =  f'for Y{year}|D{day}|{"part1" if not part2 else "part2"}'\
              f'({input_name})'

    if view: 
        view_structure=solver.export_view(structure)
        print(f'View {prefix}: {view_structure}')

    print(f'Solution {prefix}: {solution}')
    