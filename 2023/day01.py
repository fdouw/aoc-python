#!/usr/bin/env python
test_data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

test_data2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

num_str = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def parse_line(line: str):
    nums = []
    for i, c in enumerate(line):
        if c.isdigit():
            nums.append(c)
        else:
            for k, v in num_str.items():
                if line.startswith(k, i):
                    nums.append(v)
                    break
    return int(nums[0] + nums[-1])


alphabet = "abcdefghijklmnopqrstuvwxyz"
part1 = 0
part2 = 0
with open("inputs/day01", "r") as f:
    for line in f.readlines():
        stripped = line.strip().strip(alphabet)
        part1 += int(stripped[0] + stripped[-1])
        part2 += parse_line(line.strip())


print(f"Part1: {part1}")
print(f"Part2: {part2}")
