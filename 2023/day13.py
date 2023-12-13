#!/usr/bin/env python


with open("inputs/day13", "r") as f:
    patterns = f.read().split("\n\n")


part1 = 0
part2 = 0
for pat in patterns:
    lines = pat.splitlines(False)
    rows = [0] * len(lines)
    cols = [0] * len(lines[0])
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                rows[y] += 1 << x + 1  # +1 so the zeroth bit gets counted
                cols[x] += 1 << y + 1

    for i in range(len(cols) - 1):
        smudges = 0
        lo = i
        hi = i + 1
        while 0 <= lo and hi < len(cols):
            diff = cols[lo] ^ cols[hi]
            if diff.bit_count() == 1:
                smudges += 1
            elif diff.bit_count() > 1:
                smudges += 2  # definitely not a solution for part 2
            lo -= 1
            hi += 1
        if smudges == 0:
            part1 += i + 1
        elif smudges == 1:
            part2 += i + 1

    for i in range(len(rows) - 1):
        smudges = 0
        lo = i
        hi = i + 1
        while 0 <= lo and hi < len(rows):
            diff = rows[lo] ^ rows[hi]
            if diff.bit_count() == 1:
                smudges += 1
            elif diff.bit_count() > 1:
                smudges += 2  # definitely not a solution for part 2
            lo -= 1
            hi += 1
        if smudges == 0:
            part1 += (i + 1) * 100
        elif smudges == 1:
            part2 += (i + 1) * 100


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
