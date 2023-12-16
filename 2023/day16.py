#!/usr/bin/env python

# region constants

EMPTY = 0
HSPLIT = 1
VSPLIT = 2
MIRROR_FW = 3
MIRROR_BW = 4

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
        to = (WEST, SOUTH, EAST, NORTH)[dir]
        if nb := neighbour(x, y, to):
            yield nb
    elif tile == MIRROR_FW:
        to = (EAST, NORTH, WEST, SOUTH)[dir]
        if nb := neighbour(x, y, to):
            yield nb
    elif tile == HSPLIT:
        if dir == EAST or dir == WEST:
            if nb := neighbour(x, y, dir):
                yield nb
        else:
            if nb := neighbour(x, y, EAST):
                yield nb
            if nb := neighbour(x, y, WEST):
                yield nb
    elif tile == VSPLIT:
        if dir == NORTH or dir == SOUTH:
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
    visited = set()
    history = set()

    # Keep track of beams as (x,y,direction)
    # x,y is the next position to move to (ie, still unchecked)
    # direction is the direction we're moving towards
    beams = [(init_x, init_y, init_dir)]
    while beams:
        beam = beams.pop()
        x, y, dir = beam

        if beam not in history and 0 <= x < width and 0 <= y < height:
            visited.add((x, y))
            if layout[y][x] != EMPTY:
                history.add(beam)
            beams.extend(next_tiles(x, y, layout[y][x], dir))

    return len(visited)


# endregion functions

################################################################################

with open("inputs/day16", "r") as f:
    items = {".": EMPTY, "-": HSPLIT, "|": VSPLIT, "/": MIRROR_FW, "\\": MIRROR_BW}
    layout = [[items[c] for c in line.strip()] for line in f.readlines()]

width = len(layout[0])
height = len(layout)

part2 = max(
    max(trace_beam(x, 0, SOUTH) for x in range(width)),
    max(trace_beam(x, height - 1, NORTH) for x in range(width)),
    max(trace_beam(0, y, EAST) for y in range(height)),
    max(trace_beam(width - 1, y, WEST) for y in range(height)),
)


print(f"Part 1: {trace_beam(0,0,EAST)}")
print(f"Part 2: {part2}")
