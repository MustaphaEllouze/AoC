from typing import Any
from aoc.tools import ABCSolver

numbers = {
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9',
    'zero' : '0',
    '1' : '1',
    '2' : '2',
    '3' : '3',
    '4' : '4',
    '5' : '5',
    '6' : '6',
    '7' : '7',
    '8' : '8',
    '9' : '9',
    '0' : '0',
}

def find_numbers(string:str):
    
    dico = {
        n:len(string.split(n)[0])
        for n in list(numbers.keys())
        if len(string.split(n))>1
    }
    dico2 = {
        n:len(string.split(n)[-1])
        for n in list(numbers.keys())
        if len(string.split(n))>1
    }

    minn = min(
        dico.keys(),
        key=lambda x: dico[x] 
    )
    minnright = min(
        dico2.keys(),
        key=lambda x: dico2[x]
    )

    return int(numbers.get(minn, minn) + numbers.get(minnright, minnright))




class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        if not part2 :
            chiffres = [
                [
                    e
                    for e in line
                    if e.isdigit()
                ]
                for line in self.data
                ]
            
            chiffres = [
                int(e[0]+e[-1])
                for e in chiffres
            ]

            return chiffres, sum(chiffres)
        else:
            chiffres = [
                find_numbers(line)
                for line in self.data
            ]

            return chiffres, sum(chiffres)

    
    def generate_view(self, structure: Any) -> str:
        return structure
