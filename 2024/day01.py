#!/usr/bin/env python

from collections import defaultdict


left = []
right = []
with open("inputs/day01", "r") as f:
    for line in f.readlines():
        l, r = line.split()
        left.append(int(l))
        right.append(int(r))

part1 = sum((abs(l - r) for (l, r) in zip(sorted(left), sorted(right))))

num_counts = defaultdict(int)
for n in right:
    num_counts[n] += 1
part2 = sum(n * num_counts[n] for n in left)


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
