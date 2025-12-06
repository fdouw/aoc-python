#!/usr/bin/env python

from math import ceil

max_digits = 10
invalids = set()
invalids_part1 = set()
base = 1
base_hi = 10
for pattern_length in range(1, 6):
    max_repeats = ceil(max_digits / pattern_length)
    for n in range(base, base_hi):
        num = n
        for repeat in range(1, max_repeats):
            num = num * base_hi + n
            invalids.add(num)
            if repeat == 1:
                invalids_part1.add(num)
    base = base_hi
    base_hi *= 10
invalids = sorted(invalids)

part1 = 0
part2 = 0
with open("inputs/02.txt") as f:
    for id_range in f.read().split(","):
        left, right = map(int, id_range.split("-"))
        for n in invalids:
            if n < left:
                continue
            if n > right:
                break
            part2 += n
            if n in invalids_part1:
                part1 += n

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
