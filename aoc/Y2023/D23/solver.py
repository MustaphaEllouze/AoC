from typing import Any
from aoc.tools import Map, ABCSolver
import networkx
import matplotlib.pyplot as plt

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        map = Map([list(line) for line in self.data])
        starting_point = (0,1)
        finish_point = (map.height-1, map.width-2)
        
        assert map(*finish_point) == '.'

        # Function that returns the admissible neighbours for this problem
        def admissible(c:tuple[int, int])->tuple[tuple[int, int]]:
            if map(*c) == '>' and not part2: 
                neighs = [e for e in [map.right(*c)] if e is not None]
            elif map(*c) == '<' and not part2: 
                neighs = [e for e in [map.left(*c)] if e is not None]
            elif map(*c) == '^' and not part2: 
                neighs = [e for e in [map.up(*c)] if e is not None]
            elif map(*c) == 'v' and not part2: 
                neighs = [e for e in [map.down(*c)] if e is not None]
            else : # map(*c) == '.' 
                neighs = map.cardinal_neighbours(*c)
            admissible = [n for n in neighs if map(*n)!='#']
            return admissible

        # function that returns the shortest path between two points
        def shortest_path(spoint:tuple[int, int], fpoint:tuple[int, int])->int:
            to_visit = [(spoint, 0)]
            visited = []

            while to_visit : 
                c, step = to_visit.pop(0)
                if c in visited : continue
                if c == fpoint : return step
                visited.append(c)
                _admissible = admissible(c)
                for a in _admissible : 
                    to_visit.append((a, step+1))
        
        def find_closest_bifurcations(
            spoint:tuple[int, int], 
            l_bifurcations:tuple[tuple[int]]
        ):
            to_visit = [(spoint, 0, [spoint])]
            visited = []
            found_bifurcations = []

            while len(found_bifurcations)<3 and to_visit:
                c, step, the_path = to_visit.pop(0)
                if c in visited : continue
                # if c in found_bifurcations : continue
                if c in l_bifurcations and not c == spoint: 
                    found_bifurcations.append((c, step))
                    continue
                visited.append(c)
                _admissible = [n for n in admissible(c) if n not in the_path]
                for a in _admissible :
                    to_visit.append(
                        (
                            a, 
                            step+1,
                            the_path+[a],
                        )
                    )               

            return found_bifurcations
        
        # function that returns longest path between two points
        def longest_path(spoint:tuple[int, int], fpoint:tuple[int, int])->int:# # current_point, step_taken, #visited
            path = [(spoint,0, [spoint])]
            finished_path = []

            while any([e[0]!=fpoint for e in path]):
                print('Treating',len(path),'paths. Finished',len(finished_path),'paths.')
                new_iteration_path = []
                for i,p in enumerate(path) :
                    c,step,the_path = p
                    _admissible = [n for n in admissible(c) if n not in the_path]
                    for a in _admissible :
                        if a != fpoint : 
                            new_iteration_path.append((a, step+1, the_path+[a]))
                        else : 
                            finished_path.append((a, step+1, the_path+[a]))
                path = new_iteration_path
            
            return max([fp[1] for fp in finished_path])

        # Part one is easy 
        if True : return 'No structure', longest_path(starting_point, finish_point)

        # For part2, one must compute the distances between all bifurcations, faster that way
        else : 
            # Find all points that are bifurcations
            bifurcations = [
                iter
                for iter in map.iterator
                if map(*iter)!='#' and len(
                    [
                        n 
                        for n in map.cardinal_neighbours(*iter)
                        if map(*n) != '#'
                    ]
                )>2
            ]
            bifurcations.append(starting_point)
            bifurcations.append(finish_point)

            # For all bifurcation, find all bifurcations that you can reach
            # you must stop at the first one you encounter

            # Create the graph of the bifurcations and distances between them
            # The result is equal to the length  of the longest path you can 
            #   create in that graph
            
            graph = networkx.Graph()
            for b in bifurcations : 
                graph.add_node(b, pos=b)
            for b in bifurcations : 
                connect_those = find_closest_bifurcations(
                    spoint=b, l_bifurcations=bifurcations,
                )
                for node, weight in connect_those:
                    graph.add_edge(b, node, weight=weight)
            
            pos = networkx.get_node_attributes(graph, 'pos')
            networkx.draw(graph, pos)
            labels = networkx.get_edge_attributes(graph, 'weight')
            networkx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
            
            paths = networkx.all_simple_paths(graph, starting_point,finish_point)
            paths = [p for p in paths]
            lengths_of_paths = [
                sum(
                    [
                        graph.get_edge_data(n1, n2)['weight']
                        for n1, n2 in zip(p[:-1],p[1:])
                    ] 
                )
                for p in paths
            ]
            longest_path = paths[max(
                range(len(paths)),
                key=lambda x:lengths_of_paths[x],
            )]

            for (n1,n2) in zip(longest_path[:-1],longest_path[1:]):
                plt.plot([n1[0],n2[0]],[n1[1],n2[1]], color='red')         

            plt.show()
    

            return graph, max(lengths_of_paths)
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)