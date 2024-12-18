import numpy as np
from typing import Any, Self
from itertools import cycle
from enum import Enum

class DirectionEnum(Enum):
    RIGHT = 'R'
    LEFT = 'L'
    UP = 'U'
    DOWN = 'D'

    @classmethod
    def get(cls, value:str)->Self:
        return {
            'U' : DirectionEnum.UP,
            'D' : DirectionEnum.DOWN,
            'R' : DirectionEnum.RIGHT,
            'L' : DirectionEnum.LEFT,
        }.get(value, None)

class Map:
    """Represents a 2D map.
    First coordinates are lines (or Y)
    Second coordonates are columns (or X).
    0,0 is at top left corner."""
    
    def __init__(
        self,
        array:np.ndarray | list[list[Any]] = None,
        raw_data:list[str]=None,
        conversion_int:bool=False,
    ) -> None:
        """Create object from numpy array or list of lists"""
        if array :
            if isinstance(array, np.ndarray):
                self.map=array
            else:
                self.map=np.array(array)
        elif raw_data :
            self.map = np.array([list(line) for line in raw_data])
        else : 
            raise ValueError(f'Either raw_data or array must be given')

        if conversion_int :
            self.map = self.map.astype(np.int_)
    
        self.datatype = type(self(0,0))
    
    def __call__(self, line:int, column:int) -> Any:
        """Allows pseudo-subscription with parenthesis."""
        if 0<=line<self.height and 0<=column<self.width:
            return self.map[line, column]
        else:
            return None

    def __str__(self, ) -> str:
        return "\n".join(["".join([str(e) for e in line]) for line in self.map])
    
    @property
    def iterator(self, )->tuple[tuple[int]]:
        return tuple(
            (line, column)
            for line in range(self.height)
            for column in range(self.width)
        )
    
    @property
    def value_iterator(self, )->tuple[Any]:
        return tuple(
            self(*coords)
            for coords in self.iterator
        )
    
    @property
    def height(self, )->int:
        return np.shape(self.map)[0]
    
    @property
    def width(self, )->int:
        return np.shape(self.map)[1]
    
    def up(self, line:int, column:int)->tuple[int]|None:
        return (line-1, column) if 0<line<=self.height-1 and 0<=column<=self.width-1 else None
    
    def down(self, line:int, column:int)->tuple[int]|None:
        return (line+1, column) if 0<=line<self.height-1 and 0<=column<=self.width-1 else None
    
    def left(self, line:int, column:int)->tuple[int]|None:
        return (line, column-1) if 0<column<=self.width-1 and 0<=line<=self.height-1 else None
    
    def right(self, line:int, column:int)->tuple[int]|None:
        return (line, column+1) if 0<=column<self.width-1 and 0<=line<=self.height-1 else None
    
    def upright(self, line:int, column:int)->tuple[int]|None:
        up = self.up(line=line, column=column)
        if not up : return None
        return self.right(*up)
    
    def downright(self, line:int, column:int)->tuple[int]|None:
        down = self.down(line=line, column=column)
        if not down : return None
        return self.right(*down)
    
    def upleft(self, line:int, column:int)->tuple[int]|None:
        up = self.up(line=line, column=column)
        if not up : return None
        return self.left(*up)
    
    def downleft(self, line:int, column:int)->tuple[int]|None:
        down = self.down(line=line, column=column)
        if not down : return None
        return self.left(*down)
    
    def line_neighbours(self, line:int, column:int)->tuple[tuple[int]]:
            return tuple(
                [
                    neighbour
                    for neighbour in [
                        self.left(line, column),
                        self.right(line, column),
                    ]
                    if neighbour is not None
                ]
            )
    
    def column_neighbours(self, line:int, column:int)->tuple[tuple[int]]:
            return tuple(
                [
                    neighbour
                    for neighbour in [
                        self.up(line, column),
                        self.down(line, column),
                    ]
                    if neighbour is not None
                ]
            )

    def cardinal_neighbours(
            self, 
            line:int, 
            column:int, 
            filter_none:bool=True,
        )->tuple[tuple[int]]:
        unfiltered = tuple(
            [
                neighbour
                for neighbour in [
                    self.up(line, column),
                    self.down(line, column),
                    self.left(line, column),
                    self.right(line, column),
                ]
            ]
        )

        if not filter_none : return unfiltered
        else : return tuple(e for e in unfiltered if e)

    def neighbours(self, line:int, column:int)->tuple[tuple[int]]:
        list_to_check_from = [
            self.up(line, column),
            self.down(line, column),
            self.left(line, column),
            self.right(line, column),
            self.upright(line, column),
            self.downright(line, column),
            self.upleft(line, column),
            self.downleft(line, column),
        ]
        
        return tuple(
            [
                neighbour
                for neighbour in list_to_check_from
                if neighbour is not None
            ]
        )

    def inifite_iterator(self, ):
        return cycle(self.iterator)
    
    def find(self, value:Any)->tuple[int, int]|None:
        for iter in self.iterator:
            if self(*iter) == value : return iter
        return None
    
    def findall(self, value:Any)->tuple[tuple[int, int]]|None:
        finds = ()
        for iter in self.iterator:
            if self(*iter) == value : finds += ((iter),)
        if finds == () : return None
        return finds
    
    def direction_iterator(self, line:int, column:int, direction:DirectionEnum):
        match direction:
            case DirectionEnum.RIGHT : 
                return ((line, y) for y in range(column+1, self.width))
            case DirectionEnum.LEFT : 
                return ((line, y) for y in range(0, column)[::-1])
            case DirectionEnum.UP : 
                return ((x, column) for x in range(0, line)[::-1])
            case DirectionEnum.DOWN : 
                return ((x, column) for x in range(line+1, self.height))

    def find_in_direction(
            self,
            line:int,
            column:int,
            direction:str,
            value:Any,
        )->tuple[int, int]:

        for dir_neigh in self.direction_iterator(
            line=line,
            column=column,
            direction=DirectionEnum.get(value=direction)
        ) :
            if self(*dir_neigh) == value :
                return dir_neigh
        
        return None

    def is_on_edge(
            self,
            line:int,
            column:int,
    )->bool:
        return line==0 or line==self.height or column==0 or column==self.width

    def list_between_two(
            self,
            start_line:int,
            start_col:int,
            end_line:int,
            end_col:int
    )->tuple[tuple[int, int]]:
        if start_line == end_line:
            return tuple(
                (start_line, i)
                for i in range(
                    min(start_col, end_col),
                    max(start_col, end_col)+1
                )
            )
        if start_col==end_col:
            return tuple(
                (i, start_col)
                for i in range(
                    min(start_line, end_line),
                    max(start_line, end_line)+1
                )
            )
        raise NotImplementedError('Must be in line.')