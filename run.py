import sys
sys.dont_write_bytecode=1

from parameters import (
    YEAR, DAY, FILE, VIEW, PART2
)
from aoc import main

main(year=YEAR, day=DAY, other_file=FILE, view=VIEW, part2=PART2)