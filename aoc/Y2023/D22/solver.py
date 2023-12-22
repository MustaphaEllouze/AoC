from typing import Any
from aoc.tools import ABCSolver, Map, number_of_hits
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Cube : 
    x0:int
    y0:int
    z0:int
    x1:int
    y1:int
    z1:int
    direction:str = ''

    def __post_init__(self, ):
        assert (self.x0==self.x1 and self.y0==self.y1) \
            or (self.z0==self.z1 and self.y0==self.y1) \
            or (self.x0==self.x1 and self.z0==self.z1)
        
        if self.z1<self.z0 :
            (
                self.x0, self.y0, self.z0,
                self.x1, self.y1, self.z1,
            )=(
                self.x1, self.y1, self.z1,
                self.x0, self.y0, self.z0,
            )
        
        if self.x0 != self.x1 : 
            self.direction = 'x'
        elif self.y0 != self.y1 : 
            self.direction = 'y'
        elif self.z0 != self.z1 : 
            self.direction = 'z'
        else : 
            self.direction = '.'

    def fall(self, levels:int=1):
        self.z0 -= levels
        self.z1 -= levels
    
    def enumerate_coords(self)->tuple[tuple[int, int, int]]:
        return tuple(
            (x,y,z)
            for x in range(self.x0, self.x1+1)
            for y in range(self.y0, self.y1+1)
            for z in range(self.z0, self.z1+1)
        )

    def enumerate_plane_coords(self)->tuple[tuple[int, int]]:
        return tuple(
            (x,y)
            for x in range(self.x0, self.x1+1)
            for y in range(self.y0, self.y1+1)
        )
    
    def cross_in_plane(self, other:'Cube')->bool:
        return any(
            [
                coord in other.enumerate_plane_coords()
                for coord in self.enumerate_plane_coords()
            ]
        )


@dataclass
class Tetris:
    cubes:list[Cube]

    def __post_init__(self, ):
        self.cubes = sorted(
            self.cubes, 
            key=lambda x : x.z0,
        )
        self.x_min = min([min(c.x0, c.x1) for c in self.cubes])
        self.x_max = max([min(c.x0, c.x1) for c in self.cubes])

        self.y_min = min([min(c.y0, c.y1) for c in self.cubes])
        self.y_max = max([min(c.y0, c.y1) for c in self.cubes])

        self.z_min = min([min(c.z0, c.z1) for c in self.cubes])
        self.z_max = max([min(c.z0, c.z1) for c in self.cubes])

        self.map = Map(
            [
                [
                    0 
                    for _ in range(self.x_max-self.x_min+1)
                ]
                for _ in range(self.y_max-self.y_min+1)
            ]
        )
    
    def transform_coordinates(self, coords:tuple[int, int, int]):
        return (coords[1]-self.y_min, coords[0]-self.x_min)
    
    def place_cube(self, cube:Cube)->None:
        max_z =  max(
            [
                self.map(*self.transform_coordinates(coords)) 
                for coords in cube.enumerate_coords()
            ]
        )
        for coords in cube.enumerate_coords() : 
            self.map.map[*self.transform_coordinates(coords)] = max_z+1+(cube.z1-cube.z0)

    def apply_gravity(self, ):
        for cube in self.cubes : self.place_cube(cube)
    
    def place_cubes_contact(self):
        supports:dict[int, list[Cube]] = defaultdict(list)
        is_supported_by:dict[int, list[Cube]] = defaultdict(list)
        for i,cube in enumerate(self.cubes):
            cubes_under = [
                cube_u 
                for cube_u in self.cubes[:i]
                if cube.cross_in_plane(cube_u)
            ]
            if len(cubes_under) == 0 : 
                cube.fall(levels=cube.z0-1)
                continue
            max_z = max([c.z1 for c in cubes_under])
            true_cubes_under = [c for c in cubes_under if c.z1 == max_z]
            cube.fall(levels=cube.z0-max_z-1)

            for c in true_cubes_under : 
                supports[self.cubes.index(c)].append(self.cubes.index(cube))
                is_supported_by[self.cubes.index(cube)].append(self.cubes.index(c))
        
        return supports, is_supported_by


class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        cubes = [
            Cube(*[int(e) for e in line.split([',','~'])]) 
            for line in self.data
        ]
        tetris = Tetris(cubes)
        supports, issupported = tetris.place_cubes_contact()

        if not part2 : 
            result = []
            for i,_ in enumerate(tetris.cubes):
                support_this = supports[i]
                support_cubes = [issupported[j] for j in support_this]
                if all([len(liste)!=1 for liste in support_cubes]):
                    result.append(i+1)

            return tetris.cubes, len(result)
        
        else:
            result = 0
            for i,_ in enumerate(tetris.cubes):
                print(i, '//', len(tetris.cubes))
                colored = []
                to_color = [i]
                while to_color : 
                    current = to_color.pop(0)
                    if current in colored : continue
                    colored.append(current)
                    for j in supports[current] : 
                        if all([e in colored for e in issupported[j]]) : 
                            to_color.append(j)
                result += len(colored)-1
                    

            return tetris.cubes, result
    
    def generate_view(self, structure: Any) -> str:
        return '\n'.join([str(e) for e in structure])