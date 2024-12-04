#!/usr/bin/env python


from collections import defaultdict


def search(grid, x, y, dir, word):
    for i, c in enumerate(word):
        if not grid[(x + i * dir[0], y + i * dir[1])] == c:
            return False
    return True


dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

grid = defaultdict(str)
width = 0
height = 0

with open("inputs/day04", "r") as f:
    for y, line in enumerate(f.readlines()):
        height = max(y + 1, height)
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c
            width = max(x + 1, width)

# Part 1
part1 = sum(
    search(grid, x, y, d, "XMAS")
    for d in dirs
    for x in range(width)
    for y in range(height)
)

# Part 2
part2 = 0
for y in range(1, height - 1):
    for x in range(1, width - 1):
        if (
            grid[(x, y)] == "A"
            and (
                (grid[(x - 1, y - 1)] == "M" and grid[(x + 1, y + 1)] == "S")
                or (grid[(x - 1, y - 1)] == "S" and grid[(x + 1, y + 1)] == "M")
            )
            and (
                (grid[(x - 1, y + 1)] == "M" and grid[(x + 1, y - 1)] == "S")
                or (grid[(x - 1, y + 1)] == "S" and grid[(x + 1, y - 1)] == "M")
            )
        ):
            part2 += 1


# print(f"Part 1: {count}")
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
