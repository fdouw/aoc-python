#!/usr/bin/env python


def find_largest_jolt(banks: list[int], digit_count: int, start_index: int, joltage: int) -> int:
    if digit_count == 0:
        return joltage
    digit_count -= 1

    max_idx = start_index
    for i in range(start_index + 1, len(banks) - digit_count):
        if banks[i] > banks[max_idx]:
            max_idx = i

    return find_largest_jolt(banks, digit_count, max_idx + 1, 10 * joltage + banks[max_idx])


jolts = 0
jolts2 = 0
with open("inputs/03.txt") as f:
    for l in f.readlines():
        digits = list(map(int, l.strip()))
        jolts += find_largest_jolt(digits, 2, 0, 0)
        jolts2 += find_largest_jolt(digits, 12, 0, 0)

print(f"Part 1: {jolts}")
print(f"Part 2: {jolts2}")
