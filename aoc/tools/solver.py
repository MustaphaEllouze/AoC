from abc import ABC, abstractmethod, abstractclassmethod
from aoc.tools.superstring import SuperString
import os
import datetime
from typing import Any

class ABCSolver(ABC):
    def __init__(
            self, 
            folder:str,
            input_file:str,
    )->None:
        with open(f'{folder}/input/{input_file}', 'r') as f:
            self.data_unstripped = [SuperString(line) for line in f.readlines()]
            self.data = [line.strip() for line in self.data_unstripped]
        try: self.data_map_ready = [[char for char in line]for line in self.data]
        except : pass
        self.dataname = input_file
        self.folder=folder
    
    @abstractmethod
    def solve(self, part2:bool=False, )->tuple[Any, str]:
        """Returns result that should be written in AoC site.
        Returns: structure that computed solution ; solution"""
        return 'No structure', 'No solution'
    
    def export_result(self, part2:bool=False)->tuple[Any, str]:
        """Writes the result in output directory."""
        name_output_dir = f'{self.folder}/output'
        structure, solution = self.solve(part2=part2)
        if not os.path.isdir(name_output_dir):
            os.mkdir(name_output_dir)
        with open(f'{name_output_dir}/{self.dataname}', 'w') as f:
            f.write(f'{solution}\n    Solved on {datetime.datetime.now()}\n')
        return structure, solution

    @abstractmethod
    def generate_view(self, structure:Any)->str:
        """Generate a view for control."""
        return '\n'+str(structure)

    def export_view(self, structure:Any)->str:
        """Writes the view in view directory."""
        name_output_dir = f'{self.folder}/view'
        view = self.generate_view(structure)
        if not os.path.isdir(name_output_dir):
            os.mkdir(name_output_dir)
        with open(f'{name_output_dir}/{self.dataname}', 'w') as f:
            f.write(f'{view}\n    Solved on {datetime.datetime.now()}\n')
        return view