#!/usr/bin/env python

import re

with open("inputs/day19", "r") as f:
    patterns, designs = f.read().split("\n\n")
    patterns = re.compile(f"^({patterns.replace(", ","|")})+$")
    part1 = sum(1 for design in designs.splitlines() if patterns.match(design))

print(f"Part 1: {part1}")
