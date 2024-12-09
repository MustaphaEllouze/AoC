from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict
import os

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        begin = defaultdict(list)
        endin = defaultdict(list)

        beg_free = []
        end_free = []

        is_file = True

        current_mem = 0
        id = 0

        for info in self.data[0]:
            info = int(info)
            if is_file : 
                begin[id].append(current_mem)
                current_mem += info-1
                endin[id].append(current_mem)
                current_mem += 1
                id += 1
            else :
                beg_free.append(current_mem)
                current_mem += info-1
                end_free.append(current_mem)
                current_mem += 1
            is_file = not is_file

        if not part2 :
            for bf, ef in zip(beg_free, end_free):
                space = ef-bf+1
                place_from_here = bf
                left_space = space
                # print(space, place_from_here, left_space)
                while left_space > 0:
                    leftmost_byte = max(endin.values(), key=max)[-1]
                    if leftmost_byte < place_from_here : break
                    file_id = [e for e,b in endin.items() if leftmost_byte in b][0]
                    file_begin = begin[file_id][-1]
                    # print('file_begin', file_begin)
                    # print('leftmost_byte', leftmost_byte)
                    chunk_to_move = min(
                        left_space, 
                        leftmost_byte-file_begin+1
                    )
                    # print('chunk_to_move', chunk_to_move)
                    endin[file_id][-1] = leftmost_byte-chunk_to_move
                    if leftmost_byte - chunk_to_move == file_begin -1 :
                        endin[file_id].pop(-1)
                        begin[file_id].pop(-1)
                    begin[file_id].append(place_from_here)
                    endin[file_id].append(place_from_here+chunk_to_move-1)
                    begin[file_id] = sorted(begin[file_id])
                    endin[file_id] = sorted(endin[file_id])
                    place_from_here += chunk_to_move
                    left_space -= chunk_to_move
                    # print('beg_free', beg_free)
                    # print('end_free', end_free)
                    # print('\n')
                    # print('begin', begin)
                    # print('endin', endin)
        else:
            begin = {k:v[0] for k,v in begin.items()}
            endin = {k:v[0] for k,v in endin.items()}

            replaced = []

            for i, (bf, ef) in enumerate(zip(beg_free, end_free)):
                print(f'Space {i} over {len(beg_free)} ...', end='\r')
                space = ef-bf+1
                place_from_here = bf
                left_space = space
                
                # print('\n')                
                # print('begin', begin)                
                # print('endin', endin)     

                for file_id in sorted(endin.keys(), reverse=True) : 
                    len_file =  endin[file_id]-begin[file_id]+1
                    if file_id in replaced : continue
                    # print('len_file', len_file)
                    # print('left_space', left_space)
                    if begin[file_id] < place_from_here : continue
                    if len_file > left_space : continue
                    begin[file_id] = place_from_here
                    endin[file_id] = place_from_here+len_file-1
                    place_from_here = place_from_here+len_file
                    left_space -= len_file
                    replaced.append(file_id)
            
            begin = {k:[v] for k,v in begin.items()}
            endin = {k:[v] for k,v in endin.items()}
           
        
        for id_of_curr_file in begin.keys():
            for beg_mem, end_mem in zip(begin[id_of_curr_file], endin[id_of_curr_file]):
                result += sum([i*id_of_curr_file for i in range(beg_mem, end_mem+1)])
        
        return None, result


    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)