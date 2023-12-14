from typing import Any
from aoc.tools import ABCSolver, Map

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([list(line) for line in self.data])


        def go_north(
            the_map:Map,
        )->Map:
            round = [iter for iter in the_map.iterator if the_map(*iter)=='O']
            cube = [iter for iter in the_map.iterator if the_map(*iter)=='#']

            new_round = []

            for r in round :
                mini_in_col = [
                    rr 
                    for rr in sorted(new_round+cube)
                    if rr[1]==r[1] and rr[0]<r[0]
                ]
                if len(mini_in_col)>0 : 
                    rock = mini_in_col[-1]
                    new_round.append((rock[0]+1, r[1]))
                else:
                    new_round.append((0, r[1]))          

            for r in round :the_map.map[*r] = '.'
            for nr in new_round : the_map.map[*nr] = 'O'

            return the_map

        def go_west(
            the_map:Map,
        )->Map:
            round = [iter for iter in the_map.iterator if the_map(*iter)=='O']
            cube = [iter for iter in the_map.iterator if the_map(*iter)=='#']

            new_round = []

            for r in round :
                mini_in_col = [
                    rr 
                    for rr in sorted(new_round+cube)
                    if rr[0]==r[0] and rr[1]<r[1]
                ]
                if len(mini_in_col)>0 : 
                    rock = mini_in_col[-1]
                    new_round.append((r[0],rock[1]+1))
                else:
                    new_round.append((r[0], 0))     
            for r in round :the_map.map[*r] = '.'
            for nr in new_round : the_map.map[*nr] = 'O'

            return the_map
        
        def reverse_NS(the_map:Map)->Map : 
            return Map(
                [
                    line[::-1]
                    for line in the_map.map[::-1]
                ]
            )

        def go_south(
            the_map:Map,
        )->Map:
            return reverse_NS(go_north(reverse_NS(the_map)))

        def go_east(
            the_map:Map,
        )->Map:
            return reverse_NS(go_west(reverse_NS(the_map)))
        
        def score(
                the_map:Map
        )->int:
            round = [iter for iter in the_map.iterator if the_map(*iter)=='O']
            cube = [iter for iter in the_map.iterator if the_map(*iter)=='#']

            maxline = the_map.height

            return sum([maxline-r[0] for r in round])

        if not part2 : 
            return map.map, score(go_north(map))
        else:
            scores = []
            for i in range(200):
                print(i)
                map = go_east(go_south(go_west(go_north(map))))
                scores.append(score(map))

            message = r'Find the length of the cycle then find index such as '\
            r'index%length == (1e9-1)%length, and index>first number that'\
            r' starts the loop. Yes, this is cheating.'
            return map.map, (scores, message)

    def generate_view(self, structure: Any) -> str:
        result = '\n'
        for line in structure:
            for e in line : result += e
            result+='\n'
        return result