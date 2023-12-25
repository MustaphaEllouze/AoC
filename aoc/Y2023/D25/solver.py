from typing import Any
from aoc.tools import ABCSolver
from collections import defaultdict
import networkx

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        graph = networkx.Graph()

        for line in self.data : 
            splitting = line.split([':',' '])
            graph.add_node(splitting[0])
            for c in splitting[1:] : 
                graph.add_node(c)
                graph.add_edge(splitting[0],c)
        
        print(graph)

        for n1,n2 in networkx.minimum_edge_cut(graph):
            graph.remove_edge(n1,n2)
        
        print(graph)

        graph1, graph2 = networkx.connected_components(graph)

        return 'No structure', len(graph1)*len(graph2)
    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)