from typing import Any
from aoc.tools import ABCSolver, Map
from random import choice, randint

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        class PipeMap(Map):

            def __call__(self, line: int, column: int) -> Any:
                if line is None and column is None : return None
                return super().__call__(line, column)

            def pipeneighbours(self, line:int, column:int)->tuple[tuple[int]]:
                up = self.up(line, column)
                down = self.down(line, column)
                right = self.right(line, column)
                left = self.left(line, column)

                result = []

                checkup = ['S', '|', 'F', '7', None]
                checkdown = ['S', '|', 'J', 'L', None]
                checkright = ['S', '-', 'J', '7', None]
                checkleft = ['S', '-', 'L', 'F', None]

                if up is None : up=(None, None)
                if down is None : down=(None, None)
                if left is None : left=(None, None)
                if right is None : right=(None, None)

                if self(line, column) == '|' :
                    if self(*up) in checkup : result.append(up)
                    if self(*down) in checkdown : result.append(down)
                elif self(line, column) == '-':
                    if self(*right) in checkright : result.append(right)
                    if self(*left) in checkleft : result.append(left)
                elif self(line, column) == 'S':
                    if self(*up) in checkup : result.append(up)
                    if self(*down) in checkdown : result.append(down)
                    if self(*right) in checkright : result.append(right)
                    if self(*left) in checkleft : result.append(left)
                elif self(line, column) == 'F':
                    if self(*down) in checkdown : result.append(down)
                    if self(*right) in checkright : result.append(right)
                elif self(line, column) == 'J':
                    if self(*up) in checkup : result.append(up)
                    if self(*left) in checkleft : result.append(left)
                elif self(line, column) == '7':
                    if self(*left) in checkleft : result.append(left)
                    if self(*down) in checkdown : result.append(down)
                elif self(line, column) == 'L':
                    if self(*up) in checkup : result.append(up)
                    if self(*right) in checkright : result.append(right)
                else:
                    result = []
                
                return [e for e in result if (e is not None) ]

                
            
            def startingposition(self,)->tuple[int]:
                for case in self.iterator : 
                    if self(*case) == 'S':
                        return case

        pipemap = PipeMap([list(line) for line in self.data])
        start = pipemap.startingposition()
        print('start', start)

        length = 0
        current = pipemap.pipeneighbours(*start)[0]
        visited = []

        while pipemap(*current)!='S':
            visited.append(current)
            neigh = pipemap.pipeneighbours(*current)
            if length == 0 : 
                if pipemap(*neigh[0]) == 'S' : 
                    current = neigh[1]
                else:
                    current = neigh[0]
            else:
                current = [e for e in neigh if e not in visited][0]
            length += 1
    
        for iter in pipemap.iterator:
            if iter not in visited and pipemap(*iter)!='S': 
                pipemap.map[*iter] = '.'

        print('Finished calculation loop')

        if not part2 : 
            if len(visited)%2==0 : result = len(visited)//2
            else: result = len(visited)//2 +1
            return (pipemap, visited), result
        else:

            linespipemap = [list(line) for line in pipemap.map]
            linesbigpipemap = []
            for i in range(0, 2*len(linespipemap)-1):
                if i%2 == 0 : linesbigpipemap.append(linespipemap[i//2])
                else: linesbigpipemap.append(['x']*len(linespipemap[0]))
            
            lineshugepipemap = []
            for i, line in enumerate(linesbigpipemap):
                linesubhuge = []
                for j in range(0, 2*len(line)-1):
                    if j%2 == 0 : linesubhuge.append(line[j//2])
                    else: linesubhuge.append('x')
                lineshugepipemap.append(linesubhuge)

            hugepipemap = PipeMap(lineshugepipemap)

            for iter in hugepipemap.iterator :
                if hugepipemap(*iter) == '-' :
                    r = hugepipemap.right(*iter)
                    l = hugepipemap.left(*iter)
                    if (r is not None) and (hugepipemap(*r)=='x') : hugepipemap.map[*r] = '-'
                    if (l is not None) and (hugepipemap(*l)=='x') : hugepipemap.map[*l] = '-'
                elif hugepipemap(*iter) == '|' :
                    r = hugepipemap.up(*iter)
                    l = hugepipemap.down(*iter)
                    if (r is not None) and (hugepipemap(*r)=='x') : hugepipemap.map[*r] = '|'
                    if (l is not None) and (hugepipemap(*l)=='x') : hugepipemap.map[*l] = '|'
                elif hugepipemap(*iter) == 'F' :
                    r = hugepipemap.right(*iter)
                    l = hugepipemap.down(*iter)
                    if (r is not None) and (hugepipemap(*r)=='x') : hugepipemap.map[*r] = '-'
                    if (l is not None) and (hugepipemap(*l)=='x') : hugepipemap.map[*l] = '|'
                elif hugepipemap(*iter) == '7' :
                    r = hugepipemap.left(*iter)
                    l = hugepipemap.down(*iter)
                    if (r is not None) and (hugepipemap(*r)=='x') : hugepipemap.map[*r] = '-'
                    if (l is not None) and (hugepipemap(*l)=='x') : hugepipemap.map[*l] = '|'
                elif hugepipemap(*iter) == 'L' :
                    r = hugepipemap.right(*iter)
                    l = hugepipemap.up(*iter)
                    if (r is not None) and (hugepipemap(*r)=='x') : hugepipemap.map[*r] = '-'
                    if (l is not None) and (hugepipemap(*l)=='x') : hugepipemap.map[*l] = '|'
                elif hugepipemap(*iter) == 'J' :
                    r = hugepipemap.left(*iter)
                    l = hugepipemap.up(*iter)
                    if (r is not None) and (hugepipemap(*r)=='x') : hugepipemap.map[*r] = '-'
                    if (l is not None) and (hugepipemap(*l)=='x') : hugepipemap.map[*l] = '|'
            
            print('Finished treating hugemap')
            exterior = (0, 0)
            # exterior = (hugepipemap.height-1, hugepipemap.width-1)
            assert hugepipemap(*exterior) == '.'

            def currenttotovisit(current:tuple[int]):
                return f'TV,{current[0]},{current[1]}'
            def reverse(tovisit:str):
                return (int(tovisit.split(',')[1]), int(tovisit.split(',')[2]))

            count = 0
            totalatraiter = len(hugepipemap.iterator)
            for jecompte, iter in enumerate(hugepipemap.iterator) : 
                print(f'{jecompte}/{totalatraiter}')
                foundexterior = None
                if exterior == iter : foundexterior = True
                elif hugepipemap(*iter) == '.':
                    current = iter
                    foundexterior = False
                    visited = []
                    tovisit = [currenttotovisit(current)]
                    endloop = False
                    while len(tovisit)>0 and not endloop:
                        current = reverse(tovisit.pop(randint(0, len(tovisit)-1)))
                        visited.append(currenttotovisit(current))
                        tovisit += [
                            currenttotovisit(neigh) 
                            for neigh in hugepipemap.neighbours(*current) 
                            if hugepipemap(*neigh) in ['.','x','O', 'I']
                        ]
                        tovisit = list(set(tovisit).difference(set(visited)))
                        for tv in tovisit : 
                            tvtrans = reverse(tv)
                            if hugepipemap(*tvtrans) == 'O' : 
                                foundexterior = True
                                endloop = True
                            elif hugepipemap(*tvtrans) == 'I' : 
                                foundexterior = False
                                endloop = True
                            
                if foundexterior is None : continue
                if foundexterior : 
                    hugepipemap.map[*iter] = 'O'
                else : 
                    hugepipemap.map[*iter] = 'I'
                    count += 1

            return (hugepipemap, None), count
    
    def generate_view(self, structure: tuple[Map, list[tuple[int]]]) -> str:

        result = '\n'
        for line in structure[0].map : 
            for c in line : 
                result += str(c)
            result+='\n'
        return result