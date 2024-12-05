from typing import Any
from aoc.tools import ABCSolver

from collections import defaultdict

class Solver(ABCSolver):

    def solve(self, part2:bool=False) ->tuple[Any, str]:

        result = 0

        ordering = defaultdict(list)
        reverse_ordering = defaultdict(list)

        for rule in [e for e in self.data if '|' in e]:
            before, after = rule.split('|')
            ordering[before].append(after)
        
        for before,afters in ordering.items():
            for after in afters:
                reverse_ordering[after].append(before)
        
        for printing in [e for e in self.data if ',' in e]:
            pages = printing.split(',')
            printed_pages = []
            remaining_pages = [e for e in pages]
            everything_OK = True
            while remaining_pages:
                new_page = remaining_pages.pop(0)
                printed_pages.append(new_page)
                if set(ordering[new_page]).intersection(set(printed_pages))\
                    or set(reverse_ordering[new_page]).intersection(set(remaining_pages)):
                    everything_OK = False
                    remaining_pages = []
            if everything_OK and not part2:
                result += int(pages[len(pages)//2])
            elif not everything_OK and part2:
                remaining_pages = [e for e in pages]
                correct_order = []
                while remaining_pages:
                    coming_before = {
                        page:set(reverse_ordering[page]).intersection(set(remaining_pages)) 
                        for page in remaining_pages
                    }
                    page_to_put = None
                    for page,coming_after in coming_before.items():
                        if not coming_after :
                            page_to_put = page
                            break
                    remaining_pages.remove(page_to_put)
                    correct_order.append(page_to_put)
                result += int(correct_order[len(correct_order)//2])

                        

        return (ordering, reverse_ordering), result

    def generate_view(self, structure: Any) -> str:
        return super().generate_view(structure)