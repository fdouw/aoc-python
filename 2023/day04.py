#!/usr/bin/env python


points = 0
cards = []
with open("inputs/day04") as f:
    for line in f.readlines():
        _card, nums = line.split(":")
        win_nums, have_nums = map(
            lambda l: set(map(int, l.strip().replace("  ", " ").split(" "))),
            nums.split("|"),
        )
        count = len(win_nums.intersection(have_nums))
        if count > 0:
            points += 1 << (count - 1)

        # For part 2, remember the position and points for each card
        cards.append([1, count])

    for card_num, (card_count, card_points) in enumerate(cards):
        for i in range(card_num + 1, card_num + 1 + card_points):
            cards[i][0] += card_count
    part2 = sum(count for count, _ in cards)


print(f"Part 1: {points}")
print(f"Part 2: {part2}")
