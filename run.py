import sys
sys.dont_write_bytecode=1

from aoc import main as run_solver

import argparse

from datetime import datetime

def read_args()->argparse.Namespace:

    parser = argparse.ArgumentParser(
        prog='python run.py',
        description='Advent of Code - A set tools to ease Advent of Code solving, by Mustapha ELLOUZE'
    )

    parser.add_argument(
        '-y', '--year', '-Y', '--YEAR',
        help='Year of AOC to solve',
        nargs=1,
    )
    
    parser.add_argument(
        '-d', '--day', '-D', '--DAY',
        help='Day of AOC to solve',
        nargs=1,
    )
    
    parser.add_argument(
        '-i', '--input', '-I', '--INPUT',
        help='Input to solve',
        nargs=1,
    )

    parser.add_argument(
        '-v', '--view', '-V', '--VIEW',
        help='Generate a view or not',
        action='store_true'
    )
    
    parser.add_argument(
        '-p2', '--part2', '-P2', '--PART2',
        help='Specify to solve part 2',
        action='store_true'
    )
    
    parser.add_argument(
        '-b', '--both_parts', '-B', '--BOTH_PARTS',
        help='Specify to solve both parts',
        action='store_true'
    )

    return parser.parse_args()

def main():

    now = datetime.now()

    script_arguments = read_args()

    year = script_arguments.year[0] if script_arguments.year else now.year
    day = script_arguments.day[0] if script_arguments.day else now.day
    input = script_arguments.input[0] if script_arguments.input else 'input'
    view = script_arguments.view
    part2 = script_arguments.part2
    both_parts = script_arguments.both_parts

    # Run part 1
    if both_parts or not part2 :
        run_solver(
            year=year,
            day=day,
            other_file=input,
            view=view,
            part2=False
        )

    # Run part 2
    if both_parts or part2:
        run_solver(
            year=year,
            day=day,
            other_file=input,
            view=view,
            part2=True
        )

if __name__ == '__main__' : main()