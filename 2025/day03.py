#!/usr/bin/env python

jolts = 0
with open("inputs/03.txt") as f:
    for l in f.readlines():
        digits = list(map(int, l.strip()))
        i_max = 0
        for i in range(1, len(digits) - 1):
            if digits[i] > digits[i_max]:
                i_max = i
        j_max = i_max + 1
        for j in range(i_max + 2, len(digits)):
            if digits[j] > digits[j_max]:
                j_max = j
        # jolt = 10 * i_max + j_max
        jolts += 10 * digits[i_max] + digits[j_max]

print(f"Part 1: {jolts}")
