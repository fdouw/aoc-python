#!/usr/bin/env python

from functools import reduce
from operator import mul
from pprint import pprint


def transpose(matrix: list[list[str]]) -> list[list[str]]:
    new_matrix = [[item] for item in matrix[0]]
    for row in matrix[1:]:
        for i, item in enumerate(row):
            new_matrix[i].append(item)
    return new_matrix


with open("inputs/06.txt") as f:
    data = [l.split() for l in f.readlines()]
    for i in range(len(data) - 1):
        data[i] = list(map(int, data[i]))

    grand_total = 0
    for problem in transpose(data):
        operator = problem.pop()
        if operator == "+":
            grand_total += sum(problem)
        elif operator == "*":
            grand_total += reduce(mul, problem)

    # Part 2
    f.seek(0)
    grand_total2 = 0
    for block in "\n".join(map(lambda l: "".join(l).strip(), transpose(list(map(list, f.read().splitlines()))))).split(
        "\n\n"
    ):
        lines = block.splitlines()
        operator, lines[0] = lines[0][-1], lines[0][:-1]
        operands = map(int, lines)
        if operator == "+":
            grand_total2 += sum(operands)
        elif operator == "*":
            grand_total2 += reduce(mul, operands)


print(f"Part 1: {grand_total}")
print(f"Part 2: {grand_total2}")
