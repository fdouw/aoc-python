#!/usr/bin/env python

from collections import OrderedDict
import re


step_pattern = re.compile("([-=])")


with open("inputs/day15", "r") as f:
    steps = f.read().strip().split(",")


part1 = 0
for step in steps:
    value = 0
    for c in step:
        value += ord(c)
        value *= 17
    part1 += value & 255


boxes = [OrderedDict() for _ in range(256)]
for step in steps:
    label, *operation = step_pattern.split(step)

    label_hash = 0
    for c in label:
        label_hash += ord(c)
        label_hash *= 17
    box_id = label_hash & 255

    if operation[0] == "-":
        if label in boxes[box_id]:
            boxes[box_id].pop(label)
    else:
        boxes[box_id][label] = int(operation[1])

part2 = sum(
    (i + 1) * (j + 1) * lens
    for i, box in enumerate(boxes)
    for j, lens in enumerate(box.values())
)


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
