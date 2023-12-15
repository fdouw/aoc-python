#!/usr/bin/env python

# from functools import cache


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


def print_platform(platform):
    for line in platform:
        print("".join(".O#"[x] for x in line))
    print("")


def compute_load(platform):
    """Computes the load on the north beams"""
    width = len(platform[0])
    height = len(platform)

    load = 0
    for x in range(width):
        for y in range(height):
            if platform[y][x] == ROUND:
                load += height - y
    return load


# @cache
def run_cycle(platform_data: str) -> str:
    platform = [
        [parse_char(item) for item in line] for line in platform_data.splitlines(False)
    ]

    # To North
    for x in range(width):
        free = 0
        for look in range(height):
            if platform[look][x] == ROUND:
                # First clear look, then fill empty: they might be the same
                platform[look][x] = EMPTY
                platform[free][x] = ROUND

                # Find the next free spot
                free += 1
                while free < look and platform[free][x] != EMPTY:
                    free += 1
            elif platform[look][x] == CUBED:
                free = look + 1

    # To West
    for y in range(height):
        free = 0
        for look in range(width):
            if platform[y][look] == ROUND:
                # First clear look, then fill empty: they might be the same
                platform[y][look] = EMPTY
                platform[y][free] = ROUND

                # Find the next free spot
                free += 1
                while free < look and platform[y][free] != EMPTY:
                    free += 1
            elif platform[y][look] == CUBED:
                free = look + 1

    # To South
    for x in range(width):
        free = height - 1
        for look in range(height - 1, -1, -1):
            if platform[look][x] == ROUND:
                # First clear look, then fill empty: they might be the same
                platform[look][x] = EMPTY
                platform[free][x] = ROUND

                # Find the next free spot
                free -= 1
                while free > look and platform[free][x] != EMPTY:
                    free -= 1
            elif platform[look][x] == CUBED:
                free = look - 1

    # To East
    for y in range(height):
        free = width - 1
        for look in range(width - 1, -1, -1):
            if platform[y][look] == ROUND:
                # First clear look, then fill empty: they might be the same
                platform[y][look] = EMPTY
                platform[y][free] = ROUND

                # Find the next free spot
                free -= 1
                while free > look and platform[y][free] != EMPTY:
                    free -= 1
            elif platform[y][look] == CUBED:
                free = look - 1

    return "\n".join("".join(".O#"[x] for x in line) for line in platform)


# Worst case example provided by u/colecancode on Reddit:
# https://www.reddit.com/r/adventofcode/comments/18it12w/2023_day_14_part_2_custom_worst_case_testcase/
with open("inputs/day14", "r") as f:
    data = f.read()

platform = [[parse_char(item) for item in line] for line in data.splitlines(False)]
width = len(platform[0])
height = len(platform)

# Part 1
# Go column by column
# Use 2 pointers: one iterates through the column to find rocks, the other keeps track of the next available free spot
for x in range(width):
    free = 0
    for look in range(height):
        if platform[look][x] == ROUND:
            # First clear look, then fill empty: they might be the same
            platform[look][x] = EMPTY
            platform[free][x] = ROUND

            # Find the next free spot
            free += 1
            while free < look and platform[free][x] != EMPTY:
                free += 1
        elif platform[look][x] == CUBED:
            free = look + 1
part1 = compute_load(platform)

# Part 2
# 1m23.075 -> 85175
# p2_data = data
# for _ in range(1000000000):
#     p2_data = run_cycle(p2_data)
# platform = [[parse_char(item) for item in line] for line in p2_data.splitlines(False)]
# part2 = compute_load(platform)
p2_data = data
history = []
seen = {}
for idx in range(1_000_000_000):
    history.append(p2_data)
    seen[p2_data] = idx
    p2_data = run_cycle(p2_data)
    if p2_data in seen:
        prev_idx = seen[p2_data]
        period = idx + 1 - prev_idx
        remainder = (1_000_000_000 - prev_idx) % period
        p2_data = history[prev_idx + remainder]
        # print(f"Breaking at {idx + 1}")
        break
platform = [[parse_char(item) for item in line] for line in p2_data.splitlines(False)]
part2 = compute_load(platform)


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
