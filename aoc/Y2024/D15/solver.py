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
        # print([b.position for b in all_blocks_wanting])
        # print([b.movable for b in all_blocks_wanting])
        if any([not self.blocks[b].movable for b in all_blocks_wanting]):
            return
        else:
            # print('GOT HERE')
            # print('cur_pos', self.cur_pos)
            for da_block_pos,b in zip(
                    all_blocks_wanting,
                    [self.blocks[e] for e in all_blocks_wanting],
            ):
                if b.symbol == '.' : continue
                # print('CURRENTLY DISPLACING', b)
                if self.blocks[b.position] is b :
                    # print('POPED')
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
            
            # print('cur_pos', self.cur_pos)
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
            # print('direction', c)
            self.advance_one_step(
                direction=DIRECTIONS[c],
            )
            self.populate_missing()
            self.update_map()
            # print(self.map)
            # input()
    
    def get_result(self):
        result = 0
        for pos,b in self.blocks.items():
            if b.symbol == 'O' : 
                result += pos[0]*100 + pos[1]
            if b.symbol == '[':
                result += pos[0]*100
                result += pos[1]
        return result



def can_push(
        current_position:tuple[int, int],
        command:str,
        map:Map,
)->tuple[bool, tuple[int, int], tuple[int, int]]:
    closest_dot = map.find_in_direction(
        *current_position,
        direction=DIRECTIONS[command],
        value='.'
    )
    closest_wall = map.find_in_direction(
        *current_position,
        direction=DIRECTIONS[command],
        value='#'
    )
    if not closest_dot : 
        return False, None
    if abs(current_position[0]-closest_wall[0])+abs(current_position[1]-closest_wall[1]) \
        < abs(current_position[0]-closest_dot[0])+abs(current_position[1]-closest_dot[1]):
        return False, None
    return True, closest_dot

def push(
        current_position:tuple[int, int],
        command:str,
        map:Map,
        part2:bool,
        move_bonhomme:bool=True,
)->tuple[int, int]:
    print('push', current_position, command, part2, move_bonhomme)
    can_be_pushed, closest_dot = can_push(
        current_position=current_position,
        command=command,
        map=map,
    )
    if not can_be_pushed : return current_position
    if not part2:
        to_move = map.list_between_two(
                        *current_position,
                        *closest_dot,
                    )
        if DIRECTIONS[command] in ['U', 'L'] : 
            to_move = to_move[::-1]
        if move_bonhomme:
            symbols = ['.']+[map(*o) for o in to_move][:-1]
            print('MOVING THESE GUYS', to_move)
            for o,no in zip(to_move, symbols): 
                map.map[o] = no
        match DIRECTIONS[command]:
            case 'U': current_position = (current_position[0]-1, current_position[1])
            case 'D': current_position = (current_position[0]+1, current_position[1])
            case 'L': current_position = (current_position[0], current_position[1]-1)
            case 'R': current_position = (current_position[0], current_position[1]+1)
        return current_position
    else:
        if DIRECTIONS[command] in ['L', 'R']:
            return push(
                current_position=current_position, 
                command=command, 
                map=map, 
                part2=not part2,
            )
        else :
            dry_run_pos = push2(
                command=command,
                current_position=current_position,
                closest_dot=closest_dot,
                map=map,
                move_bonhomme=False
            )
            if dry_run_pos != current_position:
                return push2(
                    command=command,
                    current_position=current_position,
                    closest_dot=closest_dot,
                    map=map,
                    move_bonhomme=True,
                )
    
def push2(
        command:str,
        current_position:tuple[int, int],
        closest_dot:tuple[int, int],
        map:Map,
        move_bonhomme:bool,
)->tuple[int, int]:
    print('push2', command, current_position, closest_dot, 'DRY_RUN' if not move_bonhomme else 'WET_RUN')
    to_move = map.list_between_two(
                    *current_position,
                    *closest_dot,
                )
    if DIRECTIONS[command] == 'U' :
        to_move = to_move[::-1]
    symbols = [map(*o) for o in to_move]
    print('TRY TO MOVE THIS', to_move, symbols)
    if not '[' in symbols and not ']' in symbols:
        return push(
            current_position=current_position,
            command=command,
            map=map,
            part2=False,
            move_bonhomme=move_bonhomme,
        )
    else:
        is_down_factor = 1 if DIRECTIONS[command] == 'D' else -1
        central_future_pos = push(
                current_position=current_position,
                command=command,
                map=map,
                move_bonhomme=move_bonhomme,
                part2=False,
            )
        if central_future_pos == current_position : 
            print('CENTRAL WAS NOT MOVABLE')
            return current_position
        print('CENTER CAN BE PUSHED')
        print('ITERATING ON SYMBOLS', to_move)
        for i,pos_sym in enumerate(to_move):
            sym = map(*pos_sym)
            if sym in ['@', '.'] : continue
            elif sym == '[' :
                print('COMPUTE [')
                can_be_pushed, c_dot = can_push(
                    current_position=(
                        current_position[0]+is_down_factor*i,
                        current_position[1]+1
                    ),
                    command=command,
                    map=map,
                )
                if not can_be_pushed : return current_position
                print('CAN BE PUSHED ALONE? checking other part!')
                alrededor_future_pose = push2(
                    current_position=(
                        current_position[0]+is_down_factor*i,
                        current_position[1]+1
                    ),
                    command=command,
                    map=map,
                    move_bonhomme=move_bonhomme,
                    closest_dot=c_dot
                )
            elif sym == ']' :
                print('Compute ]')
                can_be_pushed, c_dot = can_push(
                    current_position=(
                        current_position[0]+is_down_factor*i,
                        current_position[1]-1
                    ),
                    command=command,
                    map=map,
                )
                if not can_be_pushed : return current_position
                print('CAN BE PUSHED ALONE? checking other part!!')
                alrededor_future_pose = push2(
                    current_position=(
                        current_position[0]+is_down_factor*i,
                        current_position[1]-1
                    ),
                    command=command,
                    map=map,
                    move_bonhomme=move_bonhomme,
                    closest_dot=c_dot,
                )
            else : raise NotImplementedError(f'Wrong symbol : {sym}')
            if alrededor_future_pose == current_position:
                print('this symbol is unmovable')
                return current_position
        print('EVERYTHING COULD BE PUSHED !!!!! FROM HERE', current_position)
        return central_future_pos

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

        # print(problem.map)
        # for b,bb in problem.blocks.items():
        #     print(b, bb)
        
        problem.solve()

        # cur_pos = map.find(value='@')
        # print(map)
        # for c in commands: 
        #     print('direction', c)
        #     cur_pos = push(
        #         current_position=cur_pos,
        #         command=c,
        #         map=map,
        #         part2=part2,
        #     )
        #     print(map)
        #     input()
        # if not part2:
        #     for o in map.findall('O'):
        #         result += o[0]*100+o[1]
        # else:
        #     for o in map.findall('['):
        #         result += min(o[0], map.height-o[0])*100
        #         result += min(o[1], map.width-o[1]-1)

        return problem.map, problem.get_result()
                    
    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)