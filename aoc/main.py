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
        print(f'No solver found: YEAR={year}; DAY={day}')
        quit()
    
    solver:ABCSolver=solver_class(
        folder=f'./aoc/Y{year}/D{day}',
        input_file='.input' if not other_file else f'.{other_file}',
    )

    structure, solution=solver.export_result(part2=part2)
    
    if view: 
        view_structure=solver.export_view(structure)
        print(
            f'Solution for Y{year}|D{day}({"input" if not other_file else other_file}): {view_structure}'
        )

    print(
        f'Solution for Y{year}|D{day}({"input" if not other_file else other_file}): {solution}'
    )
    