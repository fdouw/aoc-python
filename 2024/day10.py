#!/usr/bin/env python

with open("inputs/day10", "r") as f:
    grid = [list([int(c), set(), 0] for c in line) for line in f.read().splitlines()]
    height = len(grid)
    width = len(grid[0])

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
current = set()
next = set()

# Initialise search list
for y, line in enumerate(grid):
    for x, item in enumerate(line):
        if item[0] == 9:
            grid[y][x][1].add((x, y))
            grid[y][x][2] = 1
            current.add((x, y))

for h in range(8, -1, -1):
    for x, y in current:
        for dx, dy in dirs:
            if (
                0 <= x + dx < width
                and 0 <= y + dy < height
                and grid[y + dy][x + dx][0] == h
            ):
                grid[y + dy][x + dx][1] |= grid[y][x][1]
                grid[y + dy][x + dx][2] += grid[y][x][2]
                next.add((x + dx, y + dy))
    current, next = next, current
    next.clear()


# Current contains a list of coordinates of 0s and their scores
part1 = sum(len(grid[y][x][1]) for x, y in current)
part2 = sum(grid[y][x][2] for x, y in current)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
