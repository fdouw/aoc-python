#!/usr/bin/env python

with open("inputs/07.txt") as f:
    previous = list(f.readline().replace("S", "|"))
    next = ["."] * len(previous)

    # Part 1: keep track of where the beams are row by row
    split_count = 0
    skip = False
    for line in f.read().splitlines():
        for x, c in enumerate(line):
            if skip:
                skip = False
                continue
            elif c == ".":
                next[x] = previous[x]
            elif c == "^":
                if previous[x] == "|":
                    split_count += 1
                    skip = True
                    next[x - 1] = next[x + 1] = "|"
                    next[x] = "."
                else:
                    next[x] = "."

        previous, next = next, previous

    # Part 2: keep a tally of how many beams there are in each column, row by row
    f.seek(0)
    previous = [1 if c == "S" else 0 for c in f.readline()]
    next = [0] * len(previous)
    for line in f.read().splitlines():
        for x, c in enumerate(line):
            if c == ".":
                next[x] += previous[x]
            elif c == "^":
                next[x - 1] += previous[x]
                next[x + 1] += previous[x]
                next[x] = 0

        previous = next
        next = [0] * len(previous)

print(f"Part 1: {split_count}")
print(f"Part 2: {sum(previous)}")
