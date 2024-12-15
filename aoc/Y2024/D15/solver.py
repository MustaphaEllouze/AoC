from typing import Any
from aoc.tools import ABCSolver
from dataclasses import dataclass

from aoc.tools import Map

DIRECTIONS = {
            'v' : 'D',
            '^' : 'U',
            '>' : 'R',
            '<' : 'L',
        }

@dataclass
class Block:
    movable:bool
    position:tuple[int, int]
    symbol:str
    want_push:bool
    propagates:bool

class Problem:

    def __init__(
            self,
            map:Map,
            commands:list[str],
            part2:bool,
        ) -> None:
        self.blocks:dict[tuple[int, int]:Block] = {}
        for position in map.iterator:
            symbol = map(*position)
            self.blocks[position] = Block(
                movable= (symbol!='#'),
                position=position,
                symbol=symbol,
                want_push=False,
                propagates=not (symbol in ['#', '.']),
            )
        self.commands = commands
        self.map = map
        self.part2 = part2
        self.cur_pos = self.map.find(value='@')
    
    def clean_state(self):
        for bb in self.blocks.values():
            bb.want_push = False
    
    def propagate_push(
            self, 
            position:tuple[int, int],
            direction:str,
        )->list[tuple[int, int]]:
            cur_block:Block = self.blocks[position]
            if not cur_block.propagates : return []
            match direction:
                case 'L':
                    propagate_those = [self.map.left(*position)]
                case 'R':
                    propagate_those = [self.map.right(*position)]
                case 'D':
                    if cur_block.symbol == '[':
                        propagate_those = [
                            self.map.down(*position),
                            self.map.right(*self.map.down(*position)),
                            self.map.right(*position),
                        ]
                    elif cur_block.symbol == ']':
                        propagate_those = [
                            self.map.down(*position),
                            self.map.left(*self.map.down(*position)),
                            self.map.left(*position),
                        ]
                    else:
                        propagate_those = [self.map.down(*position)]
                case 'U':
                    if cur_block.symbol == '[':
                        propagate_those = [
                            self.map.up(*position),
                            self.map.right(*self.map.up(*position)),
                            self.map.right(*position),
                        ]
                    elif cur_block.symbol == ']':
                        propagate_those = [
                            self.map.up(*position),
                            self.map.left(*self.map.up(*position)),
                            self.map.left(*position),
                        ]
                    else:
                        propagate_those = [self.map.up(*position)]
            for b in propagate_those :
                self.blocks[b].want_push = True
            return propagate_those

    
    def advance_one_step(self, direction:str):
        self.clean_state()
        self.blocks[self.cur_pos].want_push = True
        to_visit = [self.cur_pos]
        visited = []
        while to_visit:
            cur_block = to_visit.pop()
            if cur_block in visited : continue
            visited.append(cur_block)
            to_visit += self.propagate_push(
                position=cur_block,
                direction=direction,
            )
        all_blocks_wanting:list[tuple[int, int]] = [
            block
            for block in visited
            if self.blocks[block].want_push
        ]
        if any([not self.blocks[b].movable for b in all_blocks_wanting]):
            return
        else:
            for b in [self.blocks[e] for e in all_blocks_wanting]:
                if b.symbol == '.' : continue
                if self.blocks[b.position] is b :
                    self.blocks.pop(b.position)
                match direction :
                    case 'U' :
                        b.position = (b.position[0]-1, b.position[1])
                    case 'D' :
                        b.position = (b.position[0]+1, b.position[1])
                    case 'L' :
                        b.position = (b.position[0], b.position[1]-1)
                    case 'R' :
                        b.position = (b.position[0], b.position[1]+1)
                self.blocks[b.position] = b 
            self.blocks[self.cur_pos] = Block(
                movable=True, position=self.cur_pos,
                symbol='.', want_push=False,
                propagates=False,
            )
            match direction:
                case 'U':
                    self.cur_pos = (self.cur_pos[0]-1, self.cur_pos[1])
                case 'D':
                    self.cur_pos = (self.cur_pos[0]+1, self.cur_pos[1])
                case 'L':
                    self.cur_pos = (self.cur_pos[0], self.cur_pos[1]-1)
                case 'R':
                    self.cur_pos = (self.cur_pos[0], self.cur_pos[1]+1)
            
    def populate_missing(self):
        for pos in self.map.iterator:
            if not pos in self.blocks.keys():
                self.blocks[pos] = Block(
                    movable=True,
                    position=pos,
                    symbol='.',
                    want_push=False,
                    propagates=False,
                )

    def update_map(self):
        for pos,b in self.blocks.items():
            self.map.map[*(b.position)] = b.symbol

    def solve(self):
        for i,c in enumerate(self.commands):
            print(f'Step {i} / {len(self.commands)}', end='\r')
            self.advance_one_step(
                direction=DIRECTIONS[c],
            )
            self.populate_missing()
            self.update_map()
    
    def get_result(self):
        result = 0
        for pos,b in self.blocks.items():
            if b.symbol == 'O' : 
                result += pos[0]*100 + pos[1]
            if b.symbol == '[':
                result += pos[0]*100
                result += pos[1]
        return result

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        split_lines = []
        split_lines2  =[]
        break_line = False

        for line in self.data :
            if line == '' : break_line = True
            if break_line : split_lines2.append(line)
            else : split_lines.append(line)
        
        if part2 :
            new_split_lines = []
            for line in split_lines:
                new_line:str = line
                new_line = new_line.replace('#', '##')
                new_line = new_line.replace('O', '[]')
                new_line = new_line.replace('.', '..')
                new_line = new_line.replace('@', '@.')
                new_split_lines.append(new_line)
            split_lines=new_split_lines

        map = Map(raw_data=split_lines)
        commands = list(''.join(split_lines2))
        print(map)

        problem = Problem(
            map=map, commands=commands, part2=part2,
        )
        
        problem.solve()

        return problem.map, problem.get_result()
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)