from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict
from itertools import combinations

import networkx as nx

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        connections : dict[str, list[str]] = defaultdict(list)

        for line in self.data:
            fc, sc = line.split('-')
            connections[fc].append(sc)
            connections[sc].append(fc)
        
        if not part2:
            three_players = defaultdict(list)

            for tcomputer, links in connections.items():
                if not tcomputer.startswith('t') : continue
                for pair1, pair2 in combinations(links, 2):
                    add = True
                    if pair1 in connections[pair2]:
                        if pair1.startswith('t') : 
                            for group in three_players[pair1]:
                                if tcomputer in group and pair2 in group:
                                    add = False
                                    break
                        if pair2.startswith('t') : 
                            for group in three_players[pair2]:
                                if tcomputer in group and pair1 in group:
                                    add = False
                                    break 
                        if add : three_players[tcomputer].append((pair1, pair2))

            return None, sum([len(e) for e in three_players.values()])
        else:
            g = nx.DiGraph()

            possible_result = None

            for c in connections : g.add_node(c)
            for line in self.data:
                fc, sc = line.split('-')
                g.add_edge(fc, sc)
            for r in range(3, g.number_of_nodes())[::-1]:
                for sub_graph in (g.subgraph(s) for s in combinations(g, r)):
                    if sub_graph.size() == r*(r-1)/2 : 
                        print(sub_graph.nodes)
                        possible_result = sub_graph
                        return None, ''.join(sorted(possible_result.nodes))

        
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)