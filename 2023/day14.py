#!/usr/bin/env python

EMPTY = 0
ROUND = 1
CUBED = 2


def parse_char(item: str) -> str:
    if item == ".":
        return EMPTY
    elif item == "O":
        return ROUND
    elif item == "#":
        return CUBED
    else:
        raise "Unknown item: {item}"


with open("inputs/day14", "r") as f:
    data = f.read().splitlines(False)

width = len(data[0])
height = len(data)
platform = [[parse_char(item) for item in line] for line in data]

# Part 1
load = 0
# Go column by column
# Use 2 pointers: one iterates through the column to find rocks, the other keeps track of the next available free spot
for x in range(width):
    free = 0
    for look in range(height):
        if platform[look][x] == ROUND:
            # First clear look, then fill empty: they might be the same
            platform[look][x] = EMPTY
            platform[free][x] = ROUND
            load += height - free

            # Find the next free spot
            free += 1
            while free < look and platform[free][x] != EMPTY:
                free += 1
        elif platform[look][x] == CUBED:
            free = look + 1

print(f"Part 1: {load}")
