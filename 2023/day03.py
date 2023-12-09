#!/usr/bin/env python

import re

pattern_num = re.compile(r"\d+")

with open("inputs/day03", "r") as f:
    # Find the symbols
    symbols = set(
        (col, row) if not (c.isdigit() or c == ".") else None
        for (row, line) in enumerate(f.readlines())
        for (col, c) in enumerate(line.strip())
    )

    # Rewind, then find all the gears: put these in a dict to collect adjacent part numbers
    f.seek(0)
    gears = dict()
    for row, line in enumerate(f.readlines()):
        for col, c in enumerate(line.strip()):
            if c == "*":
                gears[col, row] = []

    # Rewind, then iterate again to find the numbers
    f.seek(0)
    part1 = 0
    for row, line in enumerate(f.readlines()):
        for match in pattern_num.finditer(line.strip()):
            a = match.start()
            b = match.end()
            neighbours = set({(a - 1, row), (b, row)})
            for x in range(a - 1, b + 1):
                neighbours.add((x, row - 1))
                neighbours.add((x, row + 1))
            adjacent = neighbours.intersection(symbols)
            if adjacent:
                part1 += int(match[0])
                # If the symbol is a *, add the current part number
                for star in adjacent.intersection(gears.keys()):
                    gears[star].append(int(match[0]))

    part2 = sum(
        parts[0] * parts[1] if len(parts) == 2 else 0 for _, parts in gears.items()
    )

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
