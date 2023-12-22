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

def jokerize(
        original_strings: str|list[str], 
        original_character:str, 
        new_characters:list[str],
    ) -> list[str]:
    """Replace a character with a list of possible values"""
    
    if isinstance(original_strings, str) : 
        return jokerize([original_strings], original_character, new_characters)
    else:
        treatthis = [s for s in original_strings]
        result = []
        while len(treatthis)>0:
            old_guy = treatthis.pop(0)
            if original_character in old_guy:
                indexfound = old_guy.index(original_character)
                new_guys = [
                    old_guy[:indexfound]+new_c+old_guy[indexfound+1:]
                    for new_c in new_characters
                ]
                treatthis += [ng for ng in new_guys if original_character in ng]
                result += [ng for ng in new_guys if original_character not in ng]
            else:
                result.append(old_guy)
        return result

def flatten_one_level(iterable:Iterable):
    for sub_liste in iterable : assert isinstance(sub_liste, (list, tuple))
    return type(iterable)([element for sub_liste in iterable for element in sub_liste])