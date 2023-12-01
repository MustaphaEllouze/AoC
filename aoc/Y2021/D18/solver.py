from typing import Any, Self
import copy
from aoc.tools import ABCSolver


class SnailFishNumber :

    def __init__(self, number:list[list|int]) -> None:
        # print('number', number)
        value1, value2 = number[0], number[1]

        if isinstance(value1, int) : self.value1 = int(value1)
        else : self.value1 = SnailFishNumber(number=number[0])
        if isinstance(value2, int) : self.value2 = int(value2)
        else : self.value2 = SnailFishNumber(number=number[1])

    def __str__(self) -> str:
        return self.__repr__()
    
    def __repr__(self) -> str:
        return f"[{repr(self.value1)},{repr(self.value2)}]"

    @property
    def value(self):
        return eval(repr(self))
    
    @property
    def magnitude(self):
        result = 0
        if isinstance(self.value1, int) : 
            result += 3*self.value1
        else:
            result += 3*self.value1.magnitude
        
        if isinstance(self.value2, int) : 
            result += 2*self.value2
        else:
            result += 2*self.value2.magnitude
        
        return result

    def add_first_operation(self, other:Self)->Self:
        return SnailFishNumber(
            number=[self.value , other.value]
        )
    
    def iterator(self, prefix:tuple=())->tuple[int]:
        result = ()
        if isinstance(self.value1, int):
            result += (prefix+(0,),)
        else:
            subresult = self.value1.iterator(prefix=prefix+(0,))
            result += tuple(e for e in subresult)
        
        if isinstance(self.value2, int):
            result += (prefix+(1,),)
        else:
            subresult = self.value2.iterator(prefix=prefix+(1,))
            result += tuple(e for e in subresult)
        
        return result
    
    def get_value_at_index(self, index:tuple[int])->tuple[int|Self]:
        parent = None
        current = self
        for e in index :
            if e ==0:
                parent = current
                current = current.value1
            elif e == 1:
                parent = current
                current = current.value2
            else:
                raise NotImplementedError()
        return current, parent
    
    def encadrants(self, ind:tuple[int],opt_iterator:tuple[int]=None):
        if opt_iterator is None :
            itera = self.iterator()
        else:
            itera = opt_iterator
        just = itera.index(ind)
        if just > 0 : 
            just_before = itera[just-1]
        else:
            just_before = None
        if just < len(itera)-2 :
            just_after  = itera[just+2]
        else:
            just_after = None
        
        return just_before, just, just_after

    def explode(self, ind:tuple[int], opt_iterator:tuple[int]=None):
        # print(self)
        # print('explode', ind)
        if len(ind)<5 : return 
        else:
            if opt_iterator is None :
                itera = self.iterator()
            else:
                itera = opt_iterator

            just_before, just, just_after = self.encadrants(ind, itera)

            value1explode, parent = self.get_value_at_index(ind)
            value2explode = parent.value2

            if just_before is not None :
                _, totheleft = self.get_value_at_index(just_before)
                if just_before[-1] == 0 :
                    totheleft.value1 += value1explode
                else:
                    totheleft.value2 += value1explode
            
            if just_after is not None :
                _, totheright = self.get_value_at_index(just_after)
                if just_after[-1] == 0 :
                    totheright.value1 += value2explode
                else:
                    totheright.value2 += value2explode
            
            _, parent_to_replace_value = self.get_value_at_index(ind[:-1])
            if ind[-2] == 0:
                parent_to_replace_value.value1 = 0
            else:
                parent_to_replace_value.value2 = 0
        # print(just_after)
        # print(self)
        
    def split(self, ind:tuple[int], opt_iterator:tuple[int]=None):
        # print(self)
        # print('split', ind)
        if opt_iterator is None :
            itera = self.iterator()
        else:
            itera = opt_iterator

        valuesplit, parent = self.get_value_at_index(ind)

        if ind[-1] == 0:
            parent.value1 = SnailFishNumber([valuesplit//2, valuesplit-valuesplit//2])
        else:
            parent.value2 = SnailFishNumber([valuesplit//2, valuesplit-valuesplit//2])

    def explode_everybody(self, ):
        itera = self.iterator()
        incr = 0
        while incr<len(itera):
            if len(itera[incr])>=5:
                self.explode(itera[incr])
            itera = self.iterator()
            incr += 1

    def reduce(self, )->None:
        itera = self.iterator()
        incr = 0

        while incr<len(itera):

            itera = self.iterator()

            self.explode_everybody()

            itera = self.iterator()

            if self.get_value_at_index(itera[incr])[0]>=10:
                self.split(itera[incr])
                incr = 0
                continue
            
            incr += 1
        

    def add(self, other:Self)->Self:
        app = self.add_first_operation(other)
        app.reduce()
        return app



class Solver(ABCSolver):
    def solve(self, part2: bool = False) -> tuple[Any, str]:
        numbers = [
            eval(line)
            for line in self.data
        ]

        if not part2 : 

            big_number = SnailFishNumber(numbers[0])

            for ii, n in enumerate(numbers[1:]):
                print(ii, '/', len(numbers))
                # print(big_number)
                # print(n)

                big_number = big_number.add(SnailFishNumber(n))
                print(big_number)

            return 'No structure', big_number.magnitude

        else :
            best_magn = 0
            iii = 0
            for i,n in enumerate(numbers) :
                for ii, nn in enumerate(numbers[i+1:]):
                    iii += 1
                    print(iii, '/', len(numbers)*(len(numbers)-1)//2)
                    best_magn = max(
                        [
                            best_magn, 
                            SnailFishNumber(n).add(SnailFishNumber(nn)).magnitude,
                            SnailFishNumber(nn).add(SnailFishNumber(n)).magnitude,
                        ]
                    )
            
            return 'No structure', best_magn
    
    def generate_view(self, structure: Any) -> str:
        return 'No view'
