from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict

import re

from aoc.tools import Map

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        pattern = re.compile(r'p=(-?\d*),(-?\d*) v=(-?\d*),(-?\d*)')
        
        pos_x = {}
        pos_y = {}
        vel_x = {}
        vel_y = {}

        for i,robot in enumerate(self.data) :
            x, y, vx, vy = [int(e) for e in re.match(pattern, robot).groups()]
            pos_x[i] = x
            pos_y[i] = y
            vel_x[i] = vx
            vel_y[i] = vy
        
        MAX_Y = 103
        # MAX_Y = 7
        MAX_X = 101
        # MAX_X = 11
        TIME = 100

        if not part2 :
            map = Map(array=[[0 for _ in range(MAX_X)] for _ in range(MAX_Y)])

            for robot in pos_x.keys():
                pos_x[robot] = (pos_x[robot] + TIME*vel_x[robot])%MAX_X
                pos_y[robot] = (pos_y[robot] + TIME*vel_y[robot])%MAX_Y
                map.map[pos_y[robot], pos_x[robot]] += 1

            quad1 = len(
                [
                    robot
                    for robot in pos_x.keys()
                    if pos_x[robot]<MAX_X//2 and pos_y[robot]<MAX_Y//2
                ]
            )
            quad2 = len(
                [
                    robot
                    for robot in pos_x.keys()
                    if pos_x[robot]>MAX_X//2 and pos_y[robot]<MAX_Y//2
                ]
            )
            quad3 = len(
                [
                    robot
                    for robot in pos_x.keys()
                    if pos_x[robot]>MAX_X//2 and pos_y[robot]>MAX_Y//2
                ]
            )
            quad4 = len(
                [
                    robot
                    for robot in pos_x.keys()
                    if pos_x[robot]<MAX_X//2 and pos_y[robot]>MAX_Y//2
                ]
            )        

            return map, quad1*quad2*quad3*quad4
    
        else :

            TIME = 1100

            num_max_rob = max(pos_x.keys())+1

            map = Map(array=[[0 for _ in range(MAX_X)] for _ in range(MAX_Y)])
            for robot in pos_x.keys():
                pos_x[robot] = (pos_x[robot] + TIME*vel_x[robot])%MAX_X
                pos_y[robot] = (pos_y[robot] + TIME*vel_y[robot])%MAX_Y
                map.map[pos_y[robot], pos_x[robot]] += 1


            while True:
                TIME += 1
                map = Map(array=[[0 for _ in range(MAX_X)] for _ in range(MAX_Y)])
                for robot in pos_x.keys():
                    pos_x[robot] = (pos_x[robot] + vel_x[robot])%MAX_X
                    pos_y[robot] = (pos_y[robot] + vel_y[robot])%MAX_Y
                    map.map[pos_y[robot], pos_x[robot]] += 1
                
                num1 = len(map.findall(1))
                print(TIME, ' s ', num1-num_max_rob)
                if num1 == num_max_rob :
                    break
            
            return map, TIME
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)