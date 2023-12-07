#!/usr/bin/env python

from itertools import groupby

card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


class Hand:
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __init__(self, line: str) -> None:
        hand, bid = line.strip().split()
        self.bid = int(bid)
        self.hand = [card_values[c] for c in hand]
        self.hand2 = [1 if c == 11 else c for c in self.hand]  # Revalue J

        # Determine type
        no_joke = list(filter(lambda n: n != 1, self.hand2))
        groups = sorted(len(list(g)) for _, g in groupby(sorted(self.hand)))
        groups2 = sorted(len(list(g)) for _, g in groupby(sorted(no_joke)))
        if groups2:
            groups2[-1] += 5 - len(no_joke)
        else:
            groups2.append(5)
        self.type = self.find_type(groups)
        self.type2 = self.find_type(groups2)

    def find_type(self, groups: [int]) -> int:
        if groups == [5]:
            return self.FIVE_OF_A_KIND
        elif groups == [1, 4]:
            return self.FOUR_OF_A_KIND
        elif groups == [2, 3]:
            return self.FULL_HOUSE
        elif groups == [1, 1, 3]:
            return self.THREE_OF_A_KIND
        elif groups == [1, 2, 2]:
            return self.TWO_PAIR
        elif groups == [1, 1, 1, 2]:
            return self.ONE_PAIR
        elif groups == [1, 1, 1, 1, 1]:
            return self.HIGH_CARD
        else:
            print(f"NO TYPE: {self.hand} ;; {groups}")


with open("inputs/day07") as f:
    hands = [Hand(line.strip()) for line in f.readlines()]
    ranked_hands = sorted(hands, key=lambda h: (h.type, h.hand))
    ranked_hands2 = sorted(hands, key=lambda h: (h.type2, h.hand2))
    part1 = sum((rank + 1) * hand.bid for rank, hand in enumerate(ranked_hands))
    part2 = sum((rank + 1) * hand.bid for rank, hand in enumerate(ranked_hands2))

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
