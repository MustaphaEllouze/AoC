from typing import Any
from aoc.tools import ABCSolver, Map
import copy
import numpy as np

NB_STEPS=100

class Solver(ABCSolver):
    def solve(self, part2:bool=False) -> tuple[Any, str]:
        _array = [
            [
                int(octopus)
                for octopus in line
            ] 
            for line in self.data
        ]

        octomap = Map(_array)

        boolmap = Map([[False]])
        boolmap.map = copy.deepcopy(octomap.map)

        octostructure = []

        octostructure.append(copy.deepcopy(octomap.map))
        
        octoiterator = octomap.inifite_iterator()

        def compute_next_step(_octomap:Map):
            flashes = 0

            for octoflash in boolmap.iterator:
                boolmap.map[*octoflash]=False
                
            for octopus in _octomap.iterator:
                _octomap.map[*octopus] += 1
            
            nb_octupii = len(_octomap.iterator)
            nb_iterated = 0
            while(True):
                nb_iterated += 1
                octopus = next(octoiterator)
                if _octomap(*octopus)>=10 and not boolmap(*octopus):
                    boolmap.map[*octopus] = True
                    nb_iterated = 0
                    for octoneighbour in _octomap.neighbours(*octopus):
                        _octomap.map[*octoneighbour] += 1
                if nb_octupii==nb_iterated : break

            for octopus in _octomap.iterator:
                if _octomap(*octopus) >=10 :
                    _octomap.map[*octopus]=0
                    flashes+=1
            
            return _octomap, flashes

        if not part2 : 
            flashes = 0
            for _ in range(NB_STEPS):
                octomap, newflashes = compute_next_step(octomap)
                flashes += newflashes
                octostructure.append(copy.deepcopy(octomap.map))
            ###### RETOUR ##########
            return octostructure, flashes
        else:
            nb_step = 0
            while(True):
                nb_step += 1
                octomap, *_ = compute_next_step(octomap)
                octostructure.append(copy.deepcopy(octomap.map))
                if np.all(octomap.map==0): break
            return octostructure, nb_step
    
    def generate_view(self, structure: Any) -> str:
        result_string=''
        for stepmap in structure:
            result_string+=str(stepmap)+'\n'
        return result_string
