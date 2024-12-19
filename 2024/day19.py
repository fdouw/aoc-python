#!/usr/bin/env python

from functools import cache
import re


@cache
def count(design):
    if len(design) == 0:
        return 1
    else:
        return sum(count(design[len(p) :]) for p in patterns if design.startswith(p))


with open("inputs/day19", "r") as f:
    pattern_data, designs = f.read().split("\n\n")
    patterns = re.compile(f"^({pattern_data.replace(", ","|")})+$")

possible = list(filter(lambda d: patterns.match(d), designs.splitlines()))
print(f"Part 1: {len(possible)}")

patterns = list(filter(lambda p: p in ",".join(possible), pattern_data.split(", ")))
part2 = sum(map(count, possible))
print(f"Part 2: {part2}")

# for d in possible:
#     print(f"{count(d):3}: {d}")
