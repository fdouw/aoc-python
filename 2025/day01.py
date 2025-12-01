#!/usr/bin/env python

from pprint import pprint


def sign(n: int) -> int:
    if n >= 0:
        return 1
    else:
        return -1


with open("inputs/01.txt") as f:
    turns = [int(l[1:]) if l[0] == "R" else -int(l[1:]) for l in f.readlines()]


part1 = 0
dial = 50

for t in turns:
    dial = (dial + 100 + t) % 100
    if dial == 0:
        part1 += 1

print(f"{part1 = }")

part2 = 0
dial = 50
for turn in turns:
    s = sign(turn)
    full_turns, turn = divmod(abs(turn), 100)
    turn *= s
    delta = full_turns

    next_dial = dial + turn
    if next_dial >= 100:
        delta += 1
    elif next_dial <= 0 and dial > 0:
        delta += 1

    # print(f"{turn:3}\t{next_dial % 100}\t{delta = }")
    dial = next_dial % 100
    part2 += delta

print(f"{part2 = }")
