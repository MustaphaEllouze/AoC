from typing import Any
from aoc.tools import ABCSolver, Map
import copy

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([list(line) for line in self.data])
        initial_point = map.find('S')
        map.map[*initial_point] = '.'

        def compute_result_from_source(
                map:Map, 
                source:tuple[int, int],
                steps:int,
                offset:int=0,
            )->tuple[Map, int]:

            _map = Map(copy.deepcopy(map.map))

            to_visit = [(source,0)]
            visited = []
            result = []

            while to_visit:
                coords,step = to_visit.pop(0)
                if (step-offset)%2 == steps%2 and not coords in result: 
                    result.append(coords)
                if step == steps : continue
                if coords in visited : continue
                visited.append(coords)
                next_ones = _map.cardinal_neighbours(*coords)
                to_visit += [(e, step+1) for e in next_ones if _map(*e)!='#']
            
            for iter in result:
                _map.map[*iter] = 'O'

            return _map.map, len(result)


        if not part2 : 

            return compute_result_from_source(
                map=map, source=initial_point, steps=12
            )
            

        else:
            #               26501365
            # nb_steps = 2*5+2
            nb_steps = 202300*131+65

            # L'hypothèse est que le départ est le centre, de la carte centrale
            center_map = initial_point[0]
            
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
            # --> p_max est pair
            assert p_max%2 == 0

            # Il y a 13 types de cartes différentes à la fin de tous les pas
            # > Type 0 : Cette carte est totalement remplie (un pas sur deux)
            #       -----> 1+2*p_max*(p_max-1)
            # > Type 1,2,3,4 : Ces cartes corresponde aux coins du losange :
            #       - Placer le point sur le milieu d'une arrête, et faire 
            #           2*center_map pas au total
            #       -----> 1 par type
            # > Type 5,8,9,11 : Cette carte correspond à 1 carte sur 2 le 
            #       long du côté.
            #       - Placer le point sur un coin, et faire center_map pas
            #       -----> p_max par type
            # > Type 6,7,10,12 : Cetter carte correspond à l'autre carte sur 2
            #       le long du côté.
            #       - Placer le point sur un coin, et faire 3*center_map pas.
            #       -----> p_max - 1 par type

            # Type 0 
            print('Compute map', 1, 'over 13 maps.')
            map0, res0 = compute_result_from_source(
                map=map, 
                source=(center_map, center_map),
                steps=2*center_map,
            )
            map0b, res0b = compute_result_from_source(
                map=map, 
                source=(center_map, center_map),
                steps=2*center_map,
                offset=1
            )

            # Type 1, 2, 3, 4
            print('Compute map', 2, 'over 13 maps.')
            map2, res2 = compute_result_from_source(
                map=map, 
                source=(center_map, 0),
                steps=2*center_map,
                offset=p_max%2
            )
            print('Compute map', 3, 'over 13 maps.')
            map3, res3 = compute_result_from_source(
                map=map, 
                source=(center_map, 2*center_map),
                steps=2*center_map,
                offset=p_max%2
            )
            print('Compute map', 4, 'over 13 maps.')
            map4, res4 = compute_result_from_source(
                map=map, 
                source=(0, center_map),
                steps=2*center_map,
                offset=p_max%2
            )
            print('Compute map', 5, 'over 13 maps.')
            map1, res1 = compute_result_from_source(
                map=map, 
                source=(2*center_map, center_map),
                steps=2*center_map,
                offset=p_max%2
            )

            # Type 5, 8, 9, 11
            print('Compute map', 6, 'over 13 maps.')
            map11, res11 = compute_result_from_source(
                map=map, 
                source=(0, 0),
                steps=center_map,
                offset=(p_max+1)%2
            )
            print('Compute map', 7, 'over 13 maps.')
            map9, res9 = compute_result_from_source(
                map=map, 
                source=(0, 2*center_map),
                steps=center_map,
                offset=(p_max+1)%2
            )
            print('Compute map', 8, 'over 13 maps.')
            map5, res5 = compute_result_from_source(
                map=map, 
                source=(2*center_map, 0),
                steps=center_map,
                offset=(p_max+1)%2
            )
            print('Compute map', 9, 'over 13 maps.')
            map8, res8 = compute_result_from_source(
                map=map, 
                source=(2*center_map, 2*center_map),
                steps=center_map,
                offset=(p_max+1)%2
            )

            # Type 6, 7, 10, 12
            print('Compute map', 10, 'over 13 maps.')
            map12, res12 = compute_result_from_source(
                map=map, 
                source=(0, 0),
                steps=3*center_map,
                offset=p_max%2
            )
            print('Compute map', 11, 'over 13 maps.')
            map10, res10 = compute_result_from_source(
                map=map, 
                source=(0, 2*center_map),
                steps=3*center_map,
                offset=p_max%2
            )
            print('Compute map', 12, 'over 13 maps.')
            map6, res6 = compute_result_from_source(
                map=map, 
                source=(2*center_map, 0),
                steps=3*center_map,
                offset=p_max%2
            )
            print('Compute map', 13, 'over 13 maps.')
            map7, res7 = compute_result_from_source(
                map=map, 
                source=(2*center_map, 2*center_map),
                steps=3*center_map,
                offset=p_max%2
            )

            result = 0
            result += (1+4*((p_max-1)//2)*((p_max-1)//2+1))*res0
            result += (p_max**2)*res0b
            result += res1+res2+res3+res4
            result += p_max*(res5+res8+res9+res11)
            result += (p_max-1)*(res6+res7+res10+res12)

            return map0b, result

    def generate_view(self, structure: Any) -> str:
        result = ''
        result += "\n".join(
            "".join(str(e) for e in line)
            for line in structure
        )
        return result