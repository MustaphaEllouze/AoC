from typing import Any
from aoc.tools import ABCSolver
import networkx as nx
import matplotlib.pyplot as plt

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:
        graph = nx.Graph()
        
        for line in self.data:
            n1, n2 = line.split('-')
            if not n1 in graph.nodes :
                graph.add_node(n1)
            if not n2 in graph.nodes:
                graph.add_node(n2)
            graph.add_edge(n1, n2)
        
        ## Algo
        cnode = 'start'
        tovisit:list[tuple[str, list]] =  [
            (neinode, [cnode, neinode], False)
            for neinode in list(graph.neighbors(cnode))
        ] 

        total_paths = 0
        paths = []

        while len(tovisit)>0:
            next_node, path, visited_twice = tovisit.pop(-1)

            if next_node == 'end' :
                paths.append(path)
                total_paths += 1 
                continue
            
            for neinode in list(graph.neighbors(next_node)):
                if not part2 :
                    if not neinode.islower() or neinode not in path:
                        tovisit.append((neinode, path+[neinode], visited_twice))
                else:
                    if not neinode.islower() or neinode not in path:
                        tovisit.append((neinode, path+[neinode], visited_twice))
                    elif neinode == 'start' : continue
                    elif not visited_twice : 
                        tovisit.append((neinode, path+[neinode], True))
                    else : continue

            
        return (graph, paths), total_paths
    
    def generate_view(self, structure: Any) -> str:
        graph, paths = structure
        # draw = nx.draw(
        #     graph, 
        #     with_labels=True,
        # )
        # plt.show()
        # return str(draw)
        result = ''
        for path in paths:
            for elem in path :
                result += elem+'-'
            result=result[:-1]+'\n'
        return result[:-1]