from typing import Any
from aoc.tools import ABCSolver
from collections import defaultdict

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        def hash(sequence:str)->int:
            subresult = 0
            for c in sequence : 
                subresult += ord(c)
                subresult *= 17
                subresult %= 256
            return subresult

        data = self.data[0].split(',')

        if not part2 :
            result = 0
            for d in data : 
                result += hash(d)
        else:
            boxes = defaultdict(list)
            result = 0
            for sequence in data : 
                if '-' in sequence :
                    order = sequence[:sequence.index('-')]
                    box = hash(order)
                    for i, oo in enumerate(boxes[box]):
                        if order in oo :
                            boxes[box].pop(i)
                            break
                else:
                    assert '=' in sequence
                    order, focal = sequence.split('=')
                    box = hash(order)
                    found = False
                    for i, oo in enumerate(boxes[box]):
                        if order in oo :
                            boxes[box][i] = f'{order}|{focal}'
                            found = True
                            break
                    if not found :
                        boxes[box].append(f'{order}|{focal}')
            
            for box,contenu in boxes.items():
                for j,cont in enumerate(contenu):
                    order,focal = cont.split('|')
                    focal = int(focal)
                    result += (1+box)*(1+j)*focal


        return 'No structure', result

    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)