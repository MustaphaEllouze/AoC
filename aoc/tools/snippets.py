from typing import Iterable

def slice_iterable_by_modulo(iterable:Iterable, modulo:int)->tuple[Iterable]:
    return tuple(
        iterable[i::modulo]
        for i in range(modulo)
    )

def number_of_hits(reference:Iterable, checked:Iterable)->int:
        return sum(
              [
                int(e in reference)
                for e in checked
              ]
        )