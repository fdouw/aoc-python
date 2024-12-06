#!/usr/bin/env python

from collections import defaultdict


def move(pos, dir):
    return (pos[0] + dirs[dir][0], pos[1] + dirs[dir][1])


def in_area(pos):
    return 0 <= pos[0] < width and 0 <= pos[1] < height


def trace_guard(start, dir, limit=1_000_000):
    pos = start
    directions = defaultdict(set, {pos: {dir}})
    for _ in range(limit):
        nxt = move(pos, dir)
        if not in_area(nxt):
            return directions, outside
        if nxt in obstacles:
            dir = (dir + 1) % 4
            nxt = move(pos, dir)
        if nxt in obstacles:
            # This rotation will be enough, because this is where we came from
            dir = (dir + 1) % 4
            nxt = move(pos, dir)
        if not in_area(nxt):
            return directions, outside
        if nxt in directions and dir in directions[nxt]:
            return directions, nxt
        directions[nxt].add(dir)
        pos = nxt
    raise Exception("Oh no too long!")


# The order of these is important to make rotations work
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
outside = (-1, -1)

startdir = 0
obstacles = set()
width = 0
height = 0
start = (-1, -1)
with open("inputs/day06", "r") as f:
    for y, line in enumerate(f.readlines()):
        height = max(height, y + 1)
        for x, c in enumerate(line):
            width = max(width, x + 1)
            if c == "^":
                start = (x, y)
            elif c == "#":
                obstacles.add((x, y))


visited, _ = trace_guard(start, startdir)
print(f"Part 1: {len(visited)}")

# Part 2
obstructions = set()
for x, y in visited:
    if (x, y) != start:
        obstacles.add((x, y))
        _, location = trace_guard(start, startdir)
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
