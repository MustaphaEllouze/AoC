from typing import Any
from aoc.tools import ABCSolver

class Solver(ABCSolver) : 

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        if not part2:
            CARDS = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
            for i in range(2, 10):
                CARDS[str(i)] = i
        else:
            CARDS = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}
            for i in range(2, 10):
                CARDS[str(i)] = i

        NOJOK = [value for value in CARDS.keys() if value != "J"]


        class Hand:
            def __init__(self, hand: str) -> None:
                (
                    self.char1,
                    self.char2,
                    self.char3,
                    self.char4,
                    self.char5,
                ) = tuple(list(hand))
                self.hand = hand

                self.count = {key: 0 for key in CARDS.keys()}
                for c in hand:
                    self.count[c] += 1

            def rank(self) -> int:
                if 5 in self.count.values():
                    return 7
                elif 4 in self.count.values():
                    return 6
                elif 3 in self.count.values() and 2 in self.count.values():
                    return 5
                elif 3 in self.count.values():
                    return 4
                elif len([key for key, value in self.count.items() if value == 2]) == 2:
                    return 3
                elif 2 in self.count.values():
                    return 2
                else:
                    return 1

            def __lt__(self, other: "Hand") -> bool:
                rankself = self.rank()
                rankother = other.rank()
                if rankself > rankother:
                    return False
                elif rankself < rankother:
                    return True
                else:
                    for s, o in zip(self.hand, other.hand):
                        if CARDS[s] > CARDS[o]:
                            return False
                        elif CARDS[s] < CARDS[o]:
                            return True
                    return None

            def __eq__(self, other: "Hand") -> bool:
                return self.__lt__(other) is None


        def joker(hand: str) -> list[Hand]:
            parser = Hand(hand)
            result = [hand]
            if parser.char1 == "J":
                result = [c + h[1:] for h in result for c in NOJOK]
            if parser.char2 == "J":
                result = [h[:1] + c + h[2:] for h in result for c in NOJOK]
            if parser.char3 == "J":
                result = [h[:2] + c + h[3:] for h in result for c in NOJOK]
            if parser.char4 == "J":
                result = [h[:3] + c + h[4:] for h in result for c in NOJOK]
            if parser.char5 == "J":
                result = [h[:4] + c for h in result for c in NOJOK]
            return result


        class HandJoker:
            def __init__(self, hand: str) -> None:
                self.hand = hand
                self.hands = [Hand(jokhand) for jokhand in joker(hand)]

            def __lt__(self, other: "HandJoker") -> bool:
                rankself = max(self.hands).rank()
                rankother = max(other.hands).rank()
                if rankself > rankother:
                    return False
                elif rankself < rankother:
                    return True
                else:
                    for s, o in zip(self.hand, other.hand):
                        if CARDS[s] > CARDS[o]:
                            return False
                        elif CARDS[s] < CARDS[o]:
                            return True
                    return None

            def __eq__(self, other: "HandJoker") -> bool:
                return self.__lt__(other) is None


        hands = [line.split()[0] for line in self.data]
        bets = [int(line.split()[1]) for line in self.data]

        handspart1 = [Hand(h) for h in hands]
        handspart2 = [HandJoker(h) for h in hands]

        if not part2:
            sortedbets = sorted(
                bets,
                key=lambda x: handspart1[bets.index(x)],
            )
        else:
            sortedbets = sorted(
                bets,
                key=lambda x: handspart2[bets.index(x)],
            )
        return 'No structure', sum([(i + 1) * b for i, b in enumerate(sortedbets)])


    def generate_view(self, structure: Any) -> str:
        return 'No views'