#!/usr/bin/env python

from heapq import heappop, nsmallest


data_file = "inputs/08.txt"
max_connections = 1000


def dist(a: list[int], b: list[int]) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def value(i: int) -> int:
    while uf[i] != i:
        i = uf[i]
    return i


def connect(a: int, b: int):
    # Union Find: make sure both a and b identify as uf[a]
    a_val = value(a)
    b_val = value(b)
    uf[a] = uf[b] = uf[b_val] = a_val


with open(data_file) as f:
    junction_boxes = [list(map(int, coord.split(","))) for coord in f.readlines()]

box_count = len(junction_boxes)

# This dist matrix is symmetric, so only compute distances[i][j] for j < i
distances = nsmallest(
    max_connections * 10,
    ((dist(junction_boxes[i], junction_boxes[j]), i, j) for i in range(box_count) for j in range(i)),
)

uf = list(range(box_count))
circuit_count = box_count
for _joined in range(max_connections):
    _, i, j = heappop(distances)

    if value(i) != value(j):
        # i and j are not in the same circuit yet
        connect(i, j)
        circuit_count -= 1

# Get the circuit ID for each junction box and count the size of each junction
circuit_sizes = [0] * box_count
for i in range(box_count):
    circuit_sizes[value(i)] += 1

circuit_sizes = sorted(circuit_sizes, reverse=True)
part1 = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

# Part 2: keep going until all is connected
part2 = None
while circuit_count > 1:
    _, i, j = heappop(distances)

    if value(i) != value(j):
        # i and j are not in the same circuit yet
        connect(i, j)
        circuit_count -= 1
        if circuit_count == 1:
            part2 = junction_boxes[i][0] * junction_boxes[j][0]


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
