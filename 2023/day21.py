#!/usr/bin/env python

from scipy.optimize import curve_fit

NORTH = (0, -1)
WEST = (1, 0)
SOUTH = (0, 1)
EAST = (-1, 0)


def fit_func(x, a, b, c):
    """Template to fit the data for part 2"""
    return a * (x**2) + b * x + c


def move(pos: (int, int), dir: (int, int)) -> (int, int):
    return (pos[0] + dir[0], pos[1] + dir[1])


def project(pos: (int, int)) -> (int, int):
    return (pos[0] % xmax, pos[1] % ymax)


rocks = set()
xmax = 0
ymax = 0
with open("inputs/day21", "r") as f:
    for y, line in enumerate(f.readlines()):
        ymax = max(y, ymax)
        for x, square in enumerate(line.strip()):
            xmax = max(x, xmax)
            if square == "#":
                rocks.add((x, y))
            elif square == "S":
                start = (x, y)

xmax += 1
ymax += 1

# Part 1
# Simply run part 2 and check step 64
#
# Part 2
# The input is 131x131 and the starting point is in the centre.
# Given that there seem to be free paths to the edges, you would expect to take 131 * n + 65 steps to reach each new
# edge of the input (in the repeating pattern). It turns out that 26501365 also fits this pattern. So if there is a
# a pattern in the number of plots occupied on these intervals, then we can extrapolate.

current_visit = set()
previous_visit = {start}
history = [0]
nmax = 3

# Try the process for some initial steps
for _step_count in range(131 * (nmax - 1) + 65):
    for plot in previous_visit:
        for dir in (NORTH, WEST, SOUTH, EAST):
            nxt = move(plot, dir)
            if project(nxt) not in rocks:
                current_visit.add(nxt)
    previous_visit, current_visit = current_visit, set()
    history.append(len(previous_visit))

# Then try to extrapolate, assuming a degree of 2 (from looking at plots)
periodic_data = [history[131 * n + 65] for n in range(nmax)]
xvals = [131 * n + 65 for n in range(nmax)]
popt, _pcov = curve_fit(fit_func, xvals, periodic_data)

part1 = history[64]
part2 = fit_func(26501365, *popt)


print(f"Part 1: {part1}")
print(f"Part 2: {part2} (NB: probably needs rounding!)")
