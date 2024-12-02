#!/usr/bin/env python

from itertools import pairwise


def dec(t):
    a, b = t
    return a > b and a - b < 4


def inc(t):
    a, b = t
    return a < b and b - a < 4


def test(report):
    return all(map(dec, pairwise(report))) or all(map(inc, pairwise(report)))


def reduce_test(report):
    if test(report):
        return True
    for i in range(len(report)):
        short = report[:i] + report[i + 1 :]
        if test(short):
            return True
    return False


with open("inputs/day02") as f:
    reports = [[int(s) for s in line.split()] for line in f.readlines()]

print(f"Part 1: {sum(map(test,reports))}")
print(f"Part 2: {sum(map(reduce_test,reports))}")
