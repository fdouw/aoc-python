#!/usr/bin/env python


def move(pos, dir):
    return (pos[0] + dirs[dir][0], pos[1] + dirs[dir][1])


def in_area(pos):
    return 0 <= pos[0] < width and 0 <= pos[1] < height


def is_loop(obst, pos, dir, depth=1200):
    p = pos
    for _ in range(depth):
        if p in directions and directions[p] == dir:
            return True
        elif not in_area(p):
            return False
        nxt = move(p, dir)
        if nxt in obstacles or nxt == obst:
            dir = (dir + 1) % 4
            nxt = move(p, dir)
        if nxt in obstacles or nxt == obst:
            dir = (dir + 1) % 4
            nxt = move(p, dir)
        p = nxt
    return False


obstacles = set()
width = 0
height = 0
with open("inputs/day06", "r") as f:
    for y, line in enumerate(f.readlines()):
        height = max(height, y + 1)
        for x, c in enumerate(line):
            width = max(width, x + 1)
            if c == "^":
                pos = (x, y)
            elif c == "#":
                obstacles.add((x, y))

# The order of these is important to make rotations work
dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
dir = 0

directions = {pos: dir}
obstructions = set()
while True:
    nxt = move(pos, dir)
    if not in_area(nxt):
        break
    if nxt in obstacles:
        dir = (dir + 1) % 4
        nxt = move(pos, dir)
    if not in_area(nxt):
        break
    if nxt in obstacles:
        # This rotation will be enough, because this is where we came from
        dir = (dir + 1) % 4
        nxt = move(pos, dir)
    # Part 2
    obst = move(nxt, dir)
    if obst not in obstacles and in_area(obst):
        # Assume that we only have to test in a straight line
        if is_loop(obst, nxt, (dir + 1) % 4):
            obstructions.add(obst)
    # Register move
    directions[nxt] = dir
    pos = nxt

# print()
# for y in range(height):
#     for x in range(width):
#         p = (x, y)
#         if p in obstacles:
#             print("#", end="")
#         elif p in obstructions:
#             print("O", end="")
#         elif p in directions:
#             if directions[p] in {0, 2}:
#                 print("|", end="")
#             else:
#                 print("-", end="")
#         else:
#             print(".", end="")
#     print()
# print()

print(f"Part 1: {len(directions)}")
print(f"Part 2: {len(obstructions)}")
