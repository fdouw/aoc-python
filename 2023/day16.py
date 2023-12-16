#!/usr/bin/env python

# region constants

EMPTY = "."
HSPLIT = "-"
VSPLIT = "|"
MIRROR_FW = "/"
MIRROR_BW = "\\"

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

# endregion


# region functions


def neighbour(x: int, y: int, dir):
    # Assume x,y is in the layout's boundaries
    if dir == NORTH:
        if y > 0:
            return (x, y - 1, dir)
    elif dir == EAST:
        if x + 1 < width:
            return (x + 1, y, dir)
    elif dir == SOUTH:
        if y + 1 < height:
            return (x, y + 1, dir)
    elif dir == WEST:
        if x > 0:
            return (x - 1, y, dir)


def next_tiles(x: int, y: int, tile: str, dir):
    if tile == EMPTY:
        if nb := neighbour(x, y, dir):
            yield nb
    elif tile == MIRROR_BW:
        to = {NORTH: WEST, EAST: SOUTH, SOUTH: EAST, WEST: NORTH}[dir]
        if nb := neighbour(x, y, to):
            yield nb
    elif tile == MIRROR_FW:
        to = {NORTH: EAST, EAST: NORTH, SOUTH: WEST, WEST: SOUTH}[dir]
        if nb := neighbour(x, y, to):
            yield nb
    elif tile == HSPLIT:
        if dir in [EAST, WEST]:
            if nb := neighbour(x, y, dir):
                yield nb
        else:
            if nb := neighbour(x, y, EAST):
                yield nb
            if nb := neighbour(x, y, WEST):
                yield nb
    elif tile == VSPLIT:
        if dir in [NORTH, SOUTH]:
            if nb := neighbour(x, y, dir):
                yield nb
        else:
            if nb := neighbour(x, y, NORTH):
                yield nb
            if nb := neighbour(x, y, SOUTH):
                yield nb


def trace_beam(init_x: int, init_y: int, init_dir) -> int:
    # Keep track of the tiles that the beams pass (maybe grid is more efficient?)
    # Also keep track of history (incl. direction): there are loops in the beam patterns!
    # We need to do this separately, because beams can cross paths.
    # visited = set()
    history = set()

    # Keep track of beams as (x,y,direction)
    # x,y is the next position to move to (ie, still unchecked)
    # direction is the direction we're moving towards
    beams = [(init_x, init_y, init_dir)]
    while beams:
        x, y, dir = beams.pop()

        if (x, y, dir) not in history and 0 <= x < width and 0 <= y < height:
            # visited.add((x, y))
            history.add((x, y, dir))
            beams.extend(next_tiles(x, y, layout[y][x], dir))

    # return len(visited)
    return len(set((x, y) for x, y, _ in history))


# endregion functions

################################################################################

with open("inputs/day16", "r") as f:
    layout = [line.strip() for line in f.readlines()]

width = len(layout[0])
height = len(layout)

part2 = 0
for x in range(width):
    part2 = max(part2, trace_beam(x, 0, SOUTH))
    part2 = max(part2, trace_beam(x, height - 1, NORTH))
for y in range(height):
    part2 = max(part2, trace_beam(0, y, EAST))
    part2 = max(part2, trace_beam(width - 1, y, WEST))


print(f"Part 1: {trace_beam(0,0,EAST)}")
print(f"Part 2: {part2}")
