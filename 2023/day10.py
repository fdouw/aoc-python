#!/usr/bin/env python

from queue import SimpleQueue as queue


def find_start(data_field) -> (int, int):
    for y in range(len(data_field)):
        for x in range(len(data_field[y])):
            if data_field[y][x] == "S":
                return (x, y)


with open("inputs/day10", "r") as f:
    data_field = f.readlines()

    startx, starty = find_start(data_field)

    next = queue()
    if data_field[starty - 1][startx] in "|F7":
        next.put((1, startx, starty - 1))
    if data_field[starty][startx - 1] in "-LF":
        next.put((1, startx - 1, starty))
    if data_field[starty][startx + 1] in "-J7":
        next.put((1, startx + 1, starty))
    if data_field[starty + 1][startx] in "|LJ":
        next.put((1, startx, starty + 1))

    farthest = 0
    visited = set((startx, starty))
    while not next.empty():
        dist, pipex, pipey = next.get()
        visited.add((pipex, pipey))
        farthest = max(farthest, dist)
        if (
            pipey > 0
            and data_field[pipey - 1][pipex] in "|F7"
            and data_field[pipey][pipex] in "|LJ"
            and (pipex, pipey - 1) not in visited
        ):
            next.put((dist + 1, pipex, pipey - 1))
        if (
            pipex > 0
            and data_field[pipey][pipex - 1] in "-LF"
            and data_field[pipey][pipex] in "-J7"
            and (pipex - 1, pipey) not in visited
        ):
            next.put((dist + 1, pipex - 1, pipey))
        if (
            pipex < len(data_field[pipey]) - 1
            and data_field[pipey][pipex + 1] in "-J7"
            and data_field[pipey][pipex] in "-FL"
            and (pipex + 1, pipey) not in visited
        ):
            next.put((dist + 1, pipex + 1, pipey))
        if (
            pipey < len(data_field) - 1
            and data_field[pipey + 1][pipex] in "|LJ"
            and data_field[pipey][pipex] in "|F7"
            and (pipex, pipey + 1) not in visited
        ):
            next.put((dist + 1, pipex, pipey + 1))

print(f"Part 1: {farthest}")
