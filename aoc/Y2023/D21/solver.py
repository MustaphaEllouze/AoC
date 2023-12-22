from typing import Any
from aoc.tools import ABCSolver, Map, flatten_one_level

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([list(line) for line in self.data])

        if not part2 : 
            max_steps = 64

            to_visit = [(map.find('S'),0)]
            visited = []
            result = []

            while to_visit:
                coords,step = to_visit.pop(0)
                if step%2 == max_steps%2 and not coords in result: 
                    result.append(coords)
                if step == max_steps : continue
                if coords in visited : continue
                visited.append(coords)
                next_ones = map.cardinal_neighbours(*coords)
                to_visit += [(e, step+1) for e in next_ones if map(*e)!='#']
            
            for iter in result:
                map.map[*iter] = 'O'

            return map.map, len(result)

        else:
            nb_steps = 26501365

            # L'hypothèse est que le départ est le centre, de la carte centrale
            center_map = map.find('S')[0]
            
            # Calculer le nb de cartes max qu'on peut ajouter. 
            # p=0 ; q=0 est la carte du milieu 
            p_min = int((-nb_steps-center_map)/(2*center_map+1))
            p_max = int((nb_steps+center_map)/(2*center_map+1))
            q_min = p_min
            q_max = p_max

            # Vérification de l'hypothèse forte du problème 
            # --> On touche le côté est de la carte la plus à l'est
            assert center_map+p_max*(2*center_map+1) == nb_steps
            # --> On est centrés
            assert p_max + p_min == 0

            return ['No structure'], 'No solution'

    def generate_view(self, structure: Any) -> str:
        result = '\n'
        result += "\n".join(
            "".join(str(e) for e in line)
            for line in structure
        )
        return result