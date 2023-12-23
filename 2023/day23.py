#!/usr/bin/env python

import sys

sys.setrecursionlimit(10**6)

# Using these values, 3-dir switches direction 180°
NORTH = 0
WEST = 1
EAST = 2
SOUTH = 3


class Tile:
    def __init__(
        self, x: int, y: int, type: str, is_start: bool = False, is_end: bool = False
    ):
        self.x = x
        self.y = y
        self.type = type
        self.inbound = [None] * 4
        self.outbound = [None] * 4
        self.visited = False
        self.is_start = is_start
        self.is_end = is_end

    def direction_allowed(self, dir) -> bool:
        """Returns True iff moving across this tile in direction dir is allowed"""
        return self.type == "." or self.type == "^><v"[dir]

    def connect(self, dir, other, ignore_dir=False):
        """Connects this tile to other for moving in direction dir. Ie, only connect outbound for this tile and inbound
        for other. Previously connected tiles in this direction will be overwritten.
        If either self or other is directional, only connects if the direction is allowed, unless ignore_dir is True.
        """
        if ignore_dir or (self.direction_allowed(dir) and other.direction_allowed(dir)):
            self.outbound[dir] = other
            other.inbound[3 - dir] = self

    def find_path(self) -> int:
        """Recursively finds the longest path to the end tile via DFS and returns the length of the path."""
        if self.is_end:
            return 1
        else:
            self.visited = True
            path_len = 0
            for next in self.outbound:
                if next and not next.visited:
                    path_len = max(path_len, next.find_path())
            self.visited = False
            # Only add the current tile to the path if we actually found a path to the end
            return (path_len > 0) + path_len

    def trace_path(self) -> int:
        """Recursively finds the longest path to the end tile via DFS and returns the tiles comprising the path."""
        if self.is_end:
            return {self}
        else:
            self.visited = True
            paths = []
            for next in self.outbound:
                if next and not next.visited:
                    paths.append(next.trace_path())
            self.visited = False
            if paths:
                longest_path = max(paths, key=len)
                if len(longest_path) > 0:
                    longest_path.add(self)
                return longest_path
            else:
                return set()


with open("inputs/day23", "r") as f:
    tiles = {}
    tiles2 = {}
    width = 0
    height = 0
    for y, line in enumerate(f.readlines()):
        height += 1
        for x, tile in enumerate(line.strip()):
            if y == 0:
                width += 1
            if tile != "#":
                # Assume only start on the first line
                last_tile = Tile(x, y, tile, is_start=(y == 0))
                last_tile2 = Tile(x, y, tile, is_start=(y == 0))
                tiles[(x, y)] = last_tile
                tiles2[(x, y)] = last_tile2
                above = (x, y - 1)
                before = (x - 1, y)
                if above in tiles:
                    last_tile.connect(NORTH, tiles[above])
                    tiles[above].connect(SOUTH, last_tile)
                    last_tile2.connect(NORTH, tiles2[above], ignore_dir=True)
                    tiles2[above].connect(SOUTH, last_tile2, ignore_dir=True)
                if before in tiles:
                    last_tile.connect(EAST, tiles[before])
                    tiles[before].connect(WEST, last_tile)
                    last_tile2.connect(EAST, tiles2[before], ignore_dir=True)
                    tiles2[before].connect(WEST, last_tile2, ignore_dir=True)
    last_tile.is_end = True
    last_tile2.is_end = True

first_tile = (tile for tile in tiles.values() if tile.is_start).__next__()
first_tile2 = (tile for tile in tiles2.values() if tile.is_start).__next__()

# path = first_tile2.trace_path()
# print("  ", end="")
# for x in range(width):
#     print(f"{x%10}", end="")
# print()
# for y in range(height):
#     print(f"{y%10} ", end="")
#     for x in range(width):
#         pos = (x, y)
#         if pos in tiles2:
#             cur = tiles2[pos]
#             if cur in path:
#                 if cur.is_start:
#                     print("s", end="")
#                 elif cur.is_end:
#                     print("e", end="")
#                 else:
#                     print("O", end="")
#             else:
#                 if cur.is_start:
#                     print("S", end="")
#                 elif cur.is_end:
#                     print("E", end="")
#                 else:
#                     print(cur.type, end="")
#         else:
#             print("#", end="")
#     print()

# print()

# -1 to compensate double counting the starting point
print(f"Part 1: {first_tile.find_path()-1}")
print(f"Part 2: {first_tile2.find_path()-1}")
