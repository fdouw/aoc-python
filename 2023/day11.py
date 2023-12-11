#!/usr/bin/env python


def calc_offsets(coords, size, hubble=2):
    offset = 0
    offset_list = [0] * size
    for x in range(size):
        if x not in coords:
            offset += hubble - 1
        offset_list[x] = offset
    return offset_list


with open("inputs/day11", "r") as f:
    data = f.read()

    # Read the (x,y) for each galaxy and keep track of rows and columns that are occupied
    galaxies_raw = set()
    rows = set()
    cols = set()
    for y, line in enumerate(data.splitlines(keepends=False)):
        for x, pixel in enumerate(line):
            if pixel == "#":
                galaxies_raw.add((x, y))
                rows.add(y)
                cols.add(x)
    width = max(cols) + 1
    height = max(rows) + 1

    # Compute offsets for the coordinates based on empty rows and columns, then adjust the galaxies' coordinates
    row_offsets = calc_offsets(cols, width)
    col_offsets = calc_offsets(rows, height)
    galaxies = {(x + row_offsets[x], y + col_offsets[y]) for x, y in galaxies_raw}

    row_offsets = calc_offsets(cols, width, 1000000)
    col_offsets = calc_offsets(rows, height, 1000000)
    galaxies2 = {(x + row_offsets[x], y + col_offsets[y]) for x, y in galaxies_raw}

    # Compute the distances, and half it to compensate overcounting
    # Distance to itself is zero, so that doesn't matter
    part1 = sum(abs(x - u) + abs(y - v) for x, y in galaxies for u, v in galaxies) // 2
    part2 = (
        sum(abs(x - u) + abs(y - v) for x, y in galaxies2 for u, v in galaxies2) // 2
    )

print(f"Part 1: {part1}")
print(f"Part 1: {part2}")
