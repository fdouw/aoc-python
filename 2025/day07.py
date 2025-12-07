#!/usr/bin/env python

with open("inputs/07.txt") as f:
    # Going row by row
    # Part 1: count how often we split a beam
    # Part 2: keep a tally of how many beams there are in each column
    split_count = 0
    previous = [1 if c == "S" else 0 for c in f.readline()]
    next = [0] * len(previous)
    for line in f.read().splitlines():
        for x, c in enumerate(line):
            if c == ".":
                next[x] += previous[x]
            elif c == "^":
                if previous[x] > 0:
                    split_count += 1
                next[x - 1] += previous[x]
                next[x + 1] += previous[x]
                next[x] = 0
        previous = next
        next = [0] * len(previous)

print(f"Part 1: {split_count}")
print(f"Part 2: {sum(previous)}")
