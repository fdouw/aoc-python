#!/usr/bin/env python


from functools import cache


def path_count(node: str) -> int:
    if node == "out":
        return 1
    else:
        return sum(path_count(neighbour) for neighbour in network[node])


@cache
def path_count2(node: str, dac=False, fft=False) -> int:
    if node == "out":
        return 1 if dac and fft else 0
    else:
        dac |= node == "dac"
        fft |= node == "fft"
        return sum(path_count2(neighbour, dac, fft) for neighbour in network[node])


network = {}

with open("inputs/11.txt") as f:
    for line in f.readlines():
        key, vals = line.split(":")
        network[key] = list(vals.strip().split())

print(f"Part 1: {path_count("you")}")
print(f"Part 2: {path_count2("svr")}")
