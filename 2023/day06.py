#!/usr/bin/env python

import os

with open(f"inputs/day06", "r") as f:
    times = map(int, f.readline().split(":")[1].split())
    dists = map(int, f.readline().split(":")[1].split())

    part1 = 1
    for t, d in zip(times, dists):
        for x in range(t):
            if x * (t - x) > d:
                part1 *= (t + 1) - (2 * x)
                break

    # part 2
    f.seek(0)
    time = int(f.readline().split(":")[1].replace(" ", ""))
    dist = int(f.readline().split(":")[1].replace(" ", ""))
    for x in range(time):
        if x * (time - x) > dist:
            part2 = (time + 1) - (2 * x)
            break

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
