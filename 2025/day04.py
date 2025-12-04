#!/usr/bin/env python

from collections import deque

rolls = set()
with open("inputs/04.txt") as f:
    for y, l in enumerate(f.readlines()):
        for x, c in enumerate(l.strip()):
            if c == "@":
                rolls.add((x, y))

deltas = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
movable = 0
for x, y in rolls:
    if sum(1 for d in deltas if (x + d[0], y + d[1]) in rolls) < 4:
        movable += 1

print(f"Part 1: {movable}")

movable = 0
to_check = deque(rolls)
while to_check:
    x, y = to_check.popleft()
    if (x, y) in rolls and sum(1 for d in deltas if (x + d[0], y + d[1]) in rolls) < 4:
        rolls.remove((x, y))
        movable += 1
        to_check.extend((x + d[0], y + d[1]) for d in deltas)

print(f"Part 2: {movable}")
