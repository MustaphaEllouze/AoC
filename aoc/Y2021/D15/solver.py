from typing import Any
from aoc.tools import ABCSolver, Map
import networkx as nx
import matplotlib.pyplot as plt

def solve_from_map(m:Map):
    graph = nx.DiGraph()

    def name_iter(iter:tuple):
        return f'{iter[0]}-{iter[1]}' 
    
    def iter_name(name:str):
        s = name.split('-')
        return (int(s[0]), int(s[1]))

    for iter in m.iterator:
        graph.add_node(name_iter(iter))
    
    for iter in m.iterator:
        graph.add_weighted_edges_from(
            [
                (
                    name_iter(iter), 
                    name_iter(nei),
                    float(m(*nei))
                )
                for nei in m.cardinal_neighbours(*iter)
            ]
        )
    
    namestart = name_iter((0,0))
    nameend = name_iter((m.height-1, m.width-1))

    path = nx.shortest_path(graph, namestart, nameend, 'weight')

    result = sum(
        tuple(
            int(m(*iter_name(it)))
            for it in path[1:]
        )
    )    

    return (m.map, graph, path), result

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        if not part2 : 
            newmap = Map(
                [
                    list(line)
                    for line in self.data
                ]
            )
        else:
            def func(e, i, j):
                if int(e)+i+j <= 9 : return int(e)+i+j
                else:
                    return (int(e)+i+j)%10 +1
            
            newmap = Map(
                [
                    [
                        func(e,i,j)
                        for i in range(5)
                        for e in line
                    ]
                    for j in range(5)
                    for line in self.data
                ]
            )

        return solve_from_map(newmap)

        
    
    def generate_view(self, structure: Any) -> str:
        
        result=''
        for line in structure[0] : result+='\n'+str([e for e in line])
        
        return structure[2]