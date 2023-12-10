#!/usr/bin/env python

from collections import deque
from enum import Enum


Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])


def find_start(data_field) -> (int, int):
    for y in range(len(data_field)):
        for x in range(len(data_field[y])):
            if data_field[y][x] == "S":
                return (x, y)


class Grid:
    UNMARKED = 0
    LOOP = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, width: int, height: int):
        self.grid = [[self.UNMARKED] * width for _ in range(height)]
        self.width = width
        self.height = height

    def get_neighbour(self, dir: Direction, x: int, y: int) -> (int, int):
        if dir == Direction.NORTH:
            return (x, y - 1) if y > 0 else None
        elif dir == Direction.EAST:
            return (x + 1, y) if x + 1 < self.width else None
        elif dir == Direction.SOUTH:
            return (x, y + 1) if y + 1 < self.height else None
        elif dir == Direction.WEST:
            return (x - 1, y) if x > 0 else None

    def get_all_neighbours(self, x: int, y: int) -> (int, int):
        if y > 0:
            yield (x, y - 1)
        if x + 1 < self.width:
            yield (x + 1, y)
        if y + 1 < self.height:
            yield (x, y + 1)
        if x > 0:
            yield (x - 1, y)

    def mark(self, cur: (int, int), prev: (int, int) = None):
        """Marks the cell at cur = (x,y) as part of the loop. If the previous cell is not None, then also mark cells
        left and right of the loop according to the implied direction, but only if they're not part of the loop.
        """
        x, y = cur
        self.grid[y][x] = Grid.LOOP
        if not prev:
            return

        # Determine direction to mark left and right
        assert prev[0] == x or prev[1] == y
        assert prev[0] != x or prev[1] != y

        if prev[1] < y:
            # NORTH
            if nb := self.get_neighbour(Direction.EAST, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.LEFT
            if nb := self.get_neighbour(Direction.WEST, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.RIGHT
            if nb := self.get_neighbour(Direction.SOUTH, x, y):
                # Check corners
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    if data_field[y][x] == "J":
                        self.grid[nb[1]][nb[0]] = Grid.LEFT
                    if data_field[y][x] == "L":
                        self.grid[nb[1]][nb[0]] = Grid.RIGHT
        elif prev[0] > x:
            # EAST
            if nb := self.get_neighbour(Direction.SOUTH, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.LEFT
            if nb := self.get_neighbour(Direction.NORTH, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.RIGHT
            if nb := self.get_neighbour(Direction.WEST, x, y):
                # Check corners
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    if data_field[y][x] == "L":
                        self.grid[nb[1]][nb[0]] = Grid.LEFT
                    if data_field[y][x] == "F":
                        self.grid[nb[1]][nb[0]] = Grid.RIGHT
        elif prev[1] > y:
            # SOUTH
            if nb := self.get_neighbour(Direction.WEST, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.LEFT
            if nb := self.get_neighbour(Direction.EAST, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.RIGHT
            if nb := self.get_neighbour(Direction.NORTH, x, y):
                # Check corners
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    if data_field[y][x] == "F":
                        self.grid[nb[1]][nb[0]] = Grid.LEFT
                    if data_field[y][x] == "7":
                        self.grid[nb[1]][nb[0]] = Grid.RIGHT
        elif prev[0] < x:
            # WEST
            if nb := self.get_neighbour(Direction.NORTH, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.LEFT
            if nb := self.get_neighbour(Direction.SOUTH, x, y):
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    self.grid[nb[1]][nb[0]] = Grid.RIGHT
            if nb := self.get_neighbour(Direction.EAST, x, y):
                # Check corners
                if self.grid[nb[1]][nb[0]] != Grid.LOOP:
                    if data_field[y][x] == "7":
                        self.grid[nb[1]][nb[0]] = Grid.LEFT
                    if data_field[y][x] == "J":
                        self.grid[nb[1]][nb[0]] = Grid.RIGHT
        else:
            raise "Incompatible direction"

    def mark_all(self):
        """Determine which cells are left and which are right of the loop."""
        queue = deque()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] in (Grid.LEFT, Grid.RIGHT):
                    queue.append((x, y))

        left = 0
        right = 0
        while queue:
            x, y = queue.pop()
            if self.grid[y][x] == Grid.LEFT:
                left += 1
            else:
                right += 1
            for u, v in self.get_all_neighbours(x, y):
                if self.grid[v][u] == Grid.UNMARKED:
                    self.grid[v][u] = self.grid[y][x]
                    queue.appendleft((u, v))

        return (left, right)

    def print_grid(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if self.grid[y][x] == Grid.LEFT:
                    line += "L"
                elif self.grid[y][x] == Grid.RIGHT:
                    line += "R"
                elif self.grid[y][x] == Grid.LOOP:
                    line += "."
                else:
                    line += "!"
            print(line)


with open("inputs/day10", "r") as f:
    data_field = f.readlines()
    height = len(data_field)
    width = len(data_field[0])  # Assume a rectangle
    grid = Grid(width, height)

    start = find_start(data_field)
    grid.mark(start)
    startx, starty = start
    if data_field[starty - 1][startx] in "|F7":
        next = (startx, starty - 1)
    elif data_field[starty][startx - 1] in "-LF":
        next = (startx - 1, starty)
    elif data_field[starty][startx + 1] in "-J7":
        next = (startx + 1, starty)
    elif data_field[starty + 1][startx] in "|LJ":
        next = (startx, starty + 1)

    loop_len = 1
    prev = start
    while next != start:
        x, y = next
        grid.mark(next, prev)
        loop_len += 1
        if (
            y > 0
            and data_field[y - 1][x] in "|F7S"
            and data_field[y][x] in "|LJ"
            and (x, y - 1) != prev
        ):
            next = (x, y - 1)
        elif (
            x > 0
            and data_field[y][x - 1] in "-LFS"
            and data_field[y][x] in "-J7"
            and (x - 1, y) != prev
        ):
            next = (x - 1, y)
        elif (
            x < width - 1
            and data_field[y][x + 1] in "-J7S"
            and data_field[y][x] in "-FL"
            and (x + 1, y) != prev
        ):
            next = (x + 1, y)
        elif (
            y < height - 1
            and data_field[y + 1][x] in "|LJS"
            and data_field[y][x] in "|F7"
            and (x, y + 1) != prev
        ):
            next = (x, y + 1)
        else:
            raise Exception(
                f"Could not find the next step: {prev}->{next} (length: {loop_len})"
            )
        prev = (x, y)

    left, right = grid.mark_all()
    # grid.print_grid()
    # print(f"Left and right: ({left}, {right})")

    # Assume that whatever appears on the edge is not the inner part
    part2 = 0
    for x in range(grid.width):
        if grid.grid[0][x] == Grid.LEFT:
            part2 = right
            break
        if grid.grid[0][x] == Grid.RIGHT:
            part2 = left
            break

print(f"Part 1: {loop_len//2}")
print(f"Part 2: {part2}")
