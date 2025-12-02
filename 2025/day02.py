#!/usr/bin/env python

from math import ceil

invalid_id_sum = 0
with open("inputs/02.txt") as f:
    for id_range in f.read().split(","):
        left, right = map(int, id_range.split("-"))

        dim_a = ceil(len(str(left)) / 2)
        base = 10 ** (dim_a - 1)
        base_hi = 10 * base
        for n in range(base, base_hi):
            num = n + base_hi * n
            if num < left:
                continue
            if num > right:
                break
            invalid_id_sum += num

print(f"Part 1: {invalid_id_sum}")


max_digits = 10

invalids = set()
base = 1
base_hi = 10
for pattern_length in range(1, 6):
    max_repeats = ceil(max_digits / pattern_length)
    for n in range(base, base_hi):
        num = n
        for _ in range(1, max_repeats):
            num = num * base_hi + n
            invalids.add(num)
    base = base_hi
    base_hi *= 10

part2 = 0
with open("inputs/02.txt") as f:
    for id_range in f.read().split(","):
        left, right = map(int, id_range.split("-"))
        for n in range(left, right + 1):
            if n in invalids:
                part2 += n

print(f"Part 2: {part2}")
