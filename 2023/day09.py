#!/usr/bin/env python

from functools import reduce

with open("inputs/day09", "r") as f:
    part1 = 0
    part2 = 0
    for line in f.readlines():
        series = []
        series.append(list(map(int, line.strip().split())))
        while not all(x == 0 for x in series[-1]):
            series.append(
                [series[-1][i] - series[-1][i - 1] for i in range(1, len(series[-1]))]
            )
        part1 += sum([seq[-1] for seq in series])
        part2 += reduce(lambda a, b: b - a, map(lambda x: x[0], reversed(series)))

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
