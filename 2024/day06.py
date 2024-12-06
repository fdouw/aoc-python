#!/usr/bin/env python

from collections import defaultdict
from typing import Tuple


def move(pos: Tuple[int, int, int]):
    return (pos[0] + dirs[pos[2]][0], pos[1] + dirs[pos[2]][1], pos[2])


def rotate(pos, amount=1):
    return (pos[0], pos[1], (pos[2] + amount) % 4)


def in_area(pos):
    return 0 <= pos[0] < width and 0 <= pos[1] < height


def trace_guard(start, limit=1_000_000) -> Tuple[set, Tuple[int, int, int]]:
    pos = start
    directions = {pos}
    for _ in range(limit):
        nxt = move(pos)
        if not in_area(nxt):
            return directions, outside
        if (nxt[0], nxt[1]) in obstacles:
            nxt = move(rotate(pos))
        if (nxt[0], nxt[1]) in obstacles:
            # This rotation will be enough, because this is where we came from
            nxt = move(rotate(pos, amount=2))
        if not in_area(nxt):
            return directions, outside
        if nxt in directions:
            return directions, nxt
        directions.add(nxt)
        pos = nxt
    raise Exception("Oh no too long!")


# The order of these is important to make rotations work
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
outside = (-1, -1, -1)

obstacles = set()
width = 0
height = 0
start = (-1, -1, 0)
with open("inputs/day06", "r") as f:
    for y, line in enumerate(f.readlines()):
        height = max(height, y + 1)
        for x, c in enumerate(line):
            width = max(width, x + 1)
            if c == "^":
                start = (x, y, 0)
            elif c == "#":
                obstacles.add((x, y))


visited, _ = trace_guard(start)
print(f"Part 1: {len(set(map(lambda t: (t[0],t[1]), visited)))}")

# Part 2
obstructions = set()
for x, y, d in visited:
    if (x, y, 0) != start:
        obstacles.add((x, y))
        _, location = trace_guard(start)
        if location != outside:
            obstructions.add((x, y))
        obstacles.remove((x, y))
print(f"Part 2: {len(obstructions)}")

# print()
# for y in range(height):
#     for x in range(width):
#         p = (x, y)
#         if p in obstacles:
#             print("#", end="")
#         elif p in obstructions:
#             print("O", end="")
#         elif p in visited:
#             if len(visited) == 2:
#                 print("+", end="")
#             elif visited[p].isdisjoint({0, 2}):
#                 print("-", end="")
#             else:
#                 print("|", end="")
#         else:
#             print(".", end="")
#     print()
# print()
