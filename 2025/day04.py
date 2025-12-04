#!/usr/bin/env python

rolls = set()
with open("inputs/04.txt") as f:
    lines = f.readlines()
    height = len(lines)
    width = len(lines[0].strip())
    for y, l in enumerate(lines):
        for x, c in enumerate(l.strip()):
            if c == "@":
                rolls.add((x, y))

deltas = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
movable = 0
for y in range(height):
    for x in range(width):
        if (x, y) in rolls and sum(1 for d in deltas if (x + d[0], y + d[1]) in rolls) < 4:
            movable += 1

print(f"Part 1: {movable}")

repeat = True
movable = 0
while repeat:
    repeat = False
    for y in range(height):
        for x in range(width):
            if (x, y) in rolls and sum(1 for d in deltas if (x + d[0], y + d[1]) in rolls) < 4:
                repeat = True
                rolls.remove((x, y))
                movable += 1

print(f"Part 2: {movable}")
