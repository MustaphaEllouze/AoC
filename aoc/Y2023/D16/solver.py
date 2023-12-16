from typing import Any
from aoc.tools import ABCSolver, Map

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([list(line) for line in self.data])

        def compute_energized(entry_point:tuple[tuple[int], str])->int:

            current = entry_point
            visited = []
            to_visit = [current]

            while len(to_visit)>0:
                coords, direction = to_visit.pop()
                if coords is None : 
                    visited.append((coords, direction))
                    continue
                contenu = map(*coords)
                if not (coords, direction) in visited:
                    if direction == 'R':
                        match contenu :
                            case '-':
                                to_visit.append(
                                    (map.right(*coords), 'R')
                                )
                            case '|':
                                to_visit.append(
                                    (map.up(*coords), 'U')
                                )
                                to_visit.append(
                                    (map.down(*coords), 'D')
                                )
                            case '/':
                                to_visit.append(
                                    (map.up(*coords), 'U')
                                )
                            case '\\':
                                to_visit.append(
                                    (map.down(*coords), 'D')
                                )
                            case '.':
                                to_visit.append(
                                    (map.right(*coords), 'R')
                                )
                    elif direction == 'L':
                        match contenu :
                            case '-':
                                to_visit.append(
                                    (map.left(*coords), 'L')
                                )
                            case '|':
                                to_visit.append(
                                    (map.up(*coords), 'U')
                                )
                                to_visit.append(
                                    (map.down(*coords), 'D')
                                )
                            case '/':
                                to_visit.append(
                                    (map.down(*coords), 'D')
                                )
                            case '\\':
                                to_visit.append(
                                    (map.up(*coords), 'U')
                                )
                            case '.':
                                to_visit.append(
                                    (map.left(*coords), 'L')
                                )
                    elif direction == 'U':
                        match contenu :
                            case '-':
                                to_visit.append(
                                    (map.left(*coords), 'L')
                                )
                                to_visit.append(
                                    (map.right(*coords), 'R')
                                )
                            case '|':
                                to_visit.append(
                                    (map.up(*coords), 'U')
                                )
                            case '/':
                                to_visit.append(
                                    (map.right(*coords), 'R')
                                )
                            case '\\':
                                to_visit.append(
                                    (map.left(*coords), 'L')
                                )
                            case '.':
                                to_visit.append(
                                    (map.up(*coords), 'U')
                                )
                    elif direction == 'D':
                        match contenu :
                            case '-':
                                to_visit.append(
                                    (map.left(*coords), 'L')
                                )
                                to_visit.append(
                                    (map.right(*coords), 'R')
                                )
                            case '|':
                                to_visit.append(
                                    (map.down(*coords), 'D')
                                )
                            case '/':
                                to_visit.append(
                                    (map.left(*coords), 'L')
                                )
                            case '\\':
                                to_visit.append(
                                    (map.right(*coords), 'R')
                                )
                            case '.':
                                to_visit.append(
                                    (map.down(*coords), 'D')
                                )
                    else : raise NotImplementedError()
                visited.append((coords, direction))
            
            energized = [coords for coords,_ in visited if coords is not None]

            return len(set(energized))

        if not part2 : 
            return map.map, compute_energized(((0,0),'R'))
        else : 
            entry_points = []
            entry_points += [((0,i),'D') for i in range(map.width)]
            entry_points += [((map.height-1,i),'U') for i in range(map.width)]
            entry_points += [((i,0),'R') for i in range(map.height)]
            entry_points += [((i,map.width-1),'L') for i in range(map.height)]

            scores = []
            for i,e in enumerate(entry_points):
                print(i,'//',len(entry_points))
                scores.append(compute_energized(e))

            return map.map,max(scores)
    
    def generate_view(self, structure: Any) -> str:
        result = '\n'
        for line in structure:
            for e in line : result += e
            result+='\n'
        return result