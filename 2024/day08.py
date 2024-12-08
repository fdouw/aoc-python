#!/usr/bin/env python

from collections import defaultdict
from itertools import combinations


def show(height, width, antinodes, rev_antennas):
    for y in range(height):
        print()
        for x in range(width):
            if (x, y) in rev_antennas:
                print(rev_antennas[(x, y)], end="")
            elif (x, y) in antinodes:
                print("#", end="")
            else:
                print(".", end="")
    print()


with open("inputs/day08", "r") as f:
    # rev_antennas = dict()
    antennas = defaultdict(list)
    width = 0
    height = 0
    for y, line in enumerate(f.readlines()):
        height = max(height, y + 1)
        for x, c in enumerate(line.strip()):
            width = max(width, x + 1)
            if c != ".":
                antennas[c].append((x, y))
                # rev_antennas[(x, y)] = c

# show(height, width, set(), rev_antennas)

# Part 1
antinodes = set()
for locations in antennas.values():
    for a, b in combinations(locations, 2):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        p = (a[0] - dx, a[1] - dy)
        if 0 <= p[0] < width and 0 <= p[1] < height:
            antinodes.add(p)
        p = (b[0] + dx, b[1] + dy)
        if 0 <= p[0] < width and 0 <= p[1] < height:
            antinodes.add(p)
part1 = len(antinodes)

# Part 2
antinodes.clear()
for locations in antennas.values():
    for a, b in combinations(locations, 2):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        p = a
        while 0 <= p[0] < width and 0 <= p[1] < height:
            antinodes.add(p)
            p = (p[0] - dx, p[1] - dy)
        p = b
        while 0 <= p[0] < width and 0 <= p[1] < height:
            antinodes.add(p)
            p = (p[0] + dx, p[1] + dy)
part2 = len(antinodes)

# show(height, width, antinodes, rev_antennas)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
