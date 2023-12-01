import numpy as np
from typing import Any
from itertools import cycle

class Map:
    """Represents a 2D map.
    First coordinates are lines (or Y)
    Second coordonates are columns (or X).
    0,0 is at top left corner."""
    
    def __init__(
        self,
        array:np.ndarray | list[list[Any]],
    ) -> None:
        """Create object from numpy array or list of lists"""
        if isinstance(array, np.ndarray):
            self.map=array
        else:
            self.map=np.array(array)
    
        self.datatype = type(self(0,0))
    
    def __call__(self, line:int, column:int) -> Any:
        """Allows pseudo-subscription with parenthesis."""
        return self.map[line, column]
    
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
    
    def cardinal_neighbours(self, line:int, column:int)->tuple[tuple[int]]:
        return tuple(
            [
                neighbour
                for neighbour in [
                    self.up(line, column),
                    self.down(line, column),
                    self.left(line, column),
                    self.right(line, column),
                ]
                if neighbour is not None
            ]
        )

    def neighbours(self, line:int, column:int)->tuple[tuple[int]]:
        list_to_check_from = [
            self.up(line, column),
            self.down(line, column),
            self.left(line, column),
            self.right(line, column),
        ]

        if list_to_check_from[0] is not None:
            list_to_check_from += [
                self.right(*list_to_check_from[0]),
                self.left(*list_to_check_from[0]),
            ]
        if list_to_check_from[1] is not None:
            list_to_check_from += [
                self.right(*list_to_check_from[1]),
                self.left(*list_to_check_from[1]),
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