#!/usr/bin/env python

import re


mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
conditional_pattern = re.compile(r"(do)\(\)|(don't)\(\)|mul\((\d+),(\d+)\)")


with open("inputs/day03", "r") as f:
    memory = f.read()


print(f"Part 1: {sum(int(mul[0])*int(mul[1]) for mul in mul_pattern.findall(memory))}")


part2 = 0
do = True
for mempart in conditional_pattern.findall(memory):
    if mempart[0] == "do":
        do = True
    elif mempart[1] == "don't":
        do = False
    elif do:
        part2 += int(mempart[2]) * int(mempart[3])
print(f"Part 2: {part2}")
