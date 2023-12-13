#!/usr/bin/env python

from functools import cache
import re

empty_re = re.compile("[.?]*$")


@cache
def process_pattern_cache(pixels, index, current, target, runs: str):
    if target == 0:
        # No further springs allowed
        if empty_re.match(pixels, index):
            return 1
        else:
            return 0
    elif index == len(pixels):
        if current == target and runs == "0":
            return 1
        else:
            return 0
    elif pixels[index] == ".":
        if current == 0:
            return process_pattern_cache(pixels, index + 1, 0, target, runs)
        elif current != target:
            # Dead end
            return 0
        else:
            # Count this run
            target, runs = runs.split(",", 1) if runs.find(",") >= 0 else (runs, "0")
            return process_pattern_cache(pixels, index + 1, 0, int(target), runs)
    elif pixels[index] == "#":
        return process_pattern_cache(pixels, index + 1, current + 1, target, runs)
    else:
        # Wildcard
        # Substitute "#"
        count = process_pattern_cache(pixels, index + 1, current + 1, target, runs)
        # Substitute "."
        if current == 0:
            return count + process_pattern_cache(pixels, index + 1, 0, target, runs)
        elif current != target:
            return count
        else:
            target, runs = runs.split(",", 1) if runs.find(",") >= 0 else (runs, "0")
            return count + process_pattern_cache(
                pixels, index + 1, 0, int(target), runs
            )


with open("inputs/day12", "r") as f:
    part1 = 0
    part2 = 0
    for line in f.readlines():
        pixels, runs_raw = line.strip().split(" ")

        target, runs = runs_raw.split(",", 1)
        part1 += process_pattern_cache(pixels, 0, 0, int(target), runs)

        pixels = pixels + "?" + pixels + "?" + pixels + "?" + pixels + "?" + pixels
        runs_raw = (
            runs_raw + "," + runs_raw + "," + runs_raw + "," + runs_raw + "," + runs_raw
        )
        target, runs = runs_raw.split(",", 1)
        part2 += process_pattern_cache(pixels, 0, 0, int(target), runs)


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
