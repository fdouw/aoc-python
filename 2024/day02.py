#!/usr/bin/env python

from itertools import pairwise


def dec(t):
    a, b = t
    return a > b and a - b < 4


def inc(t):
    a, b = t
    return a < b and b - a < 4


def test(report):
    if all(map(dec, pairwise(report))) or all(map(inc, pairwise(report))):
        return True
    else:
        for i in range(len(report)):
            short = report[:i] + report[i + 1 :]
            if all(map(dec, pairwise(short))) or all(map(inc, pairwise(short))):
                return True
    return False


with open("inputs/day02") as f:
    reports = [[int(s) for s in line.split()] for line in f.readlines()]

print(
    f"Part 1: {sum(1 for report in reports if all(map(dec, pairwise(report)))or all(map(inc, pairwise(report))))}"
)
print(f"Part 2: {sum(1 for report in reports if test(report))}")
