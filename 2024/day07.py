#!/usr/bin/env python


def gen_sums(lefts, right, concatenate=False):
    for l in lefts:
        yield l + right
        yield l * right
        if concatenate:
            yield l * (10 ** len(str(right))) + right


equations = []
with open("inputs/day07", "r") as f:
    for line in f.readlines():
        parts = line.split(":")
        equations.append([int(parts[0]), list(map(int, parts[1].split()))])

part1 = 0
part2 = 0
for target, parts in equations:
    queue = iter(parts)
    partials = [queue.__next__()]
    partials2 = partials[:]
    for part in queue:
        partials = gen_sums(partials, part)
        partials2 = filter(
            lambda n: n <= target, gen_sums(partials2, part, concatenate=True)
        )
    if target in partials:
        part1 += target
    if target in partials2:
        part2 += target

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
