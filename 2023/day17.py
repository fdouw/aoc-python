#!/usr/bin/env python

from itertools import count
from queue import PriorityQueue


NORTH = 0 - 1j
EAST = 1 + 0j
SOUTH = 0 + 1j
WEST = -1 + 0j


with open("inputs/day17", "r") as f:
    city_map = {
        complex(x, y): loss
        for y, l in enumerate(f.readlines())
        for x, loss in enumerate(map(int, l.strip()))
    }

end_point = max(city_map, key=abs)


def search(min_run: int, max_run: int) -> int:
    # Use a counter to make the path items unique before we need to compare complex numbers:
    # complex numbers cannot be ordered, so that would raise an exception
    unique = count()
    # (hypothesis, heat loss on the path, current straight run, current direction, current position)
    paths = PriorityQueue()
    h = int(abs(end_point))
    paths.put((h, 0, 1, next(unique), EAST, 0 + 0j))
    paths.put((h, 0, 1, next(unique), SOUTH, 0 + 0j))

    history = set()

    while not paths.empty():
        _, heat_loss, run_len, _, dir, pos = paths.get()
        hist = (run_len, dir, pos)
        if hist in history:
            # We've seen a shorter path through here
            continue
        history.add(hist)
        if pos == end_point and run_len > min_run:
            # Found the path!
            return heat_loss
        pos += dir
        if pos in city_map:
            heat_loss += city_map[pos]
            h = int(abs(end_point - pos)) + heat_loss
            # Turn left and right
            if run_len >= min_run:
                paths.put((h, heat_loss, 1, next(unique), dir * 1j, pos))
                paths.put((h, heat_loss, 1, next(unique), dir * -1j, pos))
            # Go straight
            if run_len < max_run:
                paths.put((h, heat_loss, run_len + 1, next(unique), dir, pos))


print(f"Part 1: {search(0,3)}")
print(f"Part 2: {search(4,10)}")
