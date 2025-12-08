#!/usr/bin/env python

from math import sqrt


data_file = "inputs/08.txt"
max_connections = 1000


def dist(a: list[int], b: list[int]) -> int:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def value(a: int) -> int:
    i = a
    while uf[i] != i:
        i = uf[i]
    return i


def connect(a: int, b: int):
    # Union Find: make sure both a and b identify as uf[a]
    a_val = value(a)
    b_val = value(b)
    uf[a] = uf[b] = uf[b_val] = a_val


with open(data_file) as f:
    junction_boxes = [list(map(int, coord.split(","))) for coord in f.read().splitlines()]

box_count = len(junction_boxes)

# This dist matrix is symmetric, so only compute distances[i][j] for j < i
distances = sorted(
    [(dist(junction_boxes[i], junction_boxes[j]), i, j) for i in range(box_count) for j in range(i)], reverse=True
)

uf = list(range(box_count))
for _joined in range(max_connections):
    _, i, j = distances.pop()

    if value(i) != value(j):
        # i and j are not in the same circuit yet
        # print(f"Joining {junction_boxes[i]} and {junction_boxes[j]} (id {value(i)} and {value(j)})")
        connect(i, j)
    # else:
    #     print(f"Skipping {junction_boxes[i]} - {junction_boxes[j]}")

# Get the circuit ID for each junction box and count the size of each junction
circuit_sizes = [0] * box_count
for i in range(box_count):
    circuit_sizes[value(i)] += 1

circuit_sizes = sorted(circuit_sizes, reverse=True)
part1 = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

print(f"Part 1: {part1}")
