#!/usr/bin/env python

from itertools import pairwise


def area(vertices: [complex]) -> int:
    """Computes the area of a polygon from its vertices

    vertices: list of complex numbers"""
    # See: https://mathopenref.com/coordpolygonarea.html

    # Count the inside and the boundary itself
    # not sure why the boundary needs to be halved, or why we're off by 1... probably because this is a discrete problem
    # and if you imagine the vertices on the upper left corner of the squares, then half the boundary is counted and the
    # other isn't.
    vertices.append(vertices[0])
    inside = abs(
        sum(int(a.real * b.imag - a.imag * b.real) for a, b in pairwise(vertices)) // 2
    )
    boundary = sum(int(abs(a - b)) for a, b in pairwise(vertices)) // 2
    return inside + boundary + 1


dirs = (1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j)
pos1 = 0 + 0j
pos2 = 0 + 0j
vertices1 = [pos1]
vertices2 = [pos2]


with open("inputs/day18", "r") as f:
    for line in f.readlines():
        direction, distance, hex = line.split()
        # step 1
        step = dirs["RDLU".index(direction)]
        pos1 += int(distance) * step
        vertices1.append(pos1)
        # part 2
        distance = int(hex[2:7], 16)
        step = dirs[int(hex[-2])]
        pos2 += int(distance) * step
        vertices2.append(pos2)


print(f"Part 1: {area(vertices1)}")
print(f"Part 2: {area(vertices2)}")
