#!/usr/bin/env python

from functools import cache
from time import perf_counter


@cache
def parse(stone, depth):
    if depth == 0:
        return 1
    elif stone == 0:
        return parse(1, depth - 1)
    else:
        s = str(stone)
        l, r = divmod(len(s), 2)
        if r == 0:
            return parse(int(s[:l]), depth - 1) + parse(int(s[l:]), depth - 1)
        else:
            return parse(stone * 2024, depth - 1)


start = perf_counter()
with open("inputs/day11", "r") as f:
    stones = list(map(int, f.read().strip().split()))

part1 = sum(map(lambda n: parse(n, 25), stones))
part2 = sum(map(lambda n: parse(n, 75), stones))

end = perf_counter()
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
print(f"Time: {end/1000}")
