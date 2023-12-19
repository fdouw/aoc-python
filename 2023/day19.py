#!/usr/bin/env python

from functools import reduce
from queue import Queue
import re


# Answer: 128000000000000
test_data1 = """in{x<2001:A,R}

{x=1,m=1,a=1,s=1}"""

# Answer: 1
test_data2 = """in{x<4000:R,m<4000:R,a<4000:R,s<4000:R,A}

{x=1,m=1,a=1,s=1}"""

# Answer: 1
test_data3 = """in{x>1:R,m>1:R,a>1:R,s>1:R,A}

{x=1,m=1,a=1,s=1}"""

test_data4 = """in{x>2023:A,m<13:A,A}

{x=1,m=1,a=1,s=1}"""

test_data5 = """in{a<2000:A,A}

{x=1,m=1,a=1,s=1}"""


rule_split_pattern = re.compile(r"([<>:])")
rule_label_pattern = re.compile(r"^[ARa-z]+$")


class RangedRatings:
    def __init__(self, ranges=((1, 4000), (1, 4000), (1, 4000), (1, 4000))):
        self.ranges = ranges

    def __getitem__(self, index: str) -> (int, int):
        return self.ranges[index]

    def count(self) -> int:
        # return reduce(lambda a, b: a * b, map(lambda a, b: b - a + 1, self.ranges))
        diffs = [b - a + 1 for a, b in self.ranges]
        return reduce(lambda a, b: a * b, diffs)

    def split_below(self, index: int, midpoint: int):
        """Returns 2 ranges: one below midpoint (at index), the other above.
        If either is empty, returns None for that item.
        The midpoint is in the upper RangedRating."""
        if midpoint <= self.ranges[index][0]:
            return None, self
        if midpoint > self.ranges[index][1]:
            return self, None

        lo = ((self.ranges[index][0], midpoint - 1),)
        hi = ((midpoint, self.ranges[index][1]),)
        return (
            RangedRatings((self.ranges[:index] + lo + self.ranges[index + 1 :])),
            RangedRatings((self.ranges[:index] + hi + self.ranges[index + 1 :])),
        )

    def split_above(self, index: int, midpoint: int):
        """Returns 2 ranges: one below midpoint (at index), the other above.
        If either is empty, returns None for that item.
        The midpoint is in the lower RangedRating."""
        if midpoint < self.ranges[index][0]:
            return None, self
        if midpoint >= self.ranges[index][1]:
            return self, None

        lo = ((self.ranges[index][0], midpoint),)
        hi = ((midpoint + 1, self.ranges[index][1]),)
        return (
            RangedRatings((self.ranges[:index] + lo + self.ranges[index + 1 :])),
            RangedRatings((self.ranges[:index] + hi + self.ranges[index + 1 :])),
        )


def parse_rule_data(data: str):
    if rule_label_pattern.match(data):
        return data
    d = rule_split_pattern.split(data)
    return ("xmas".index(d[0]), d[1], int(d[2]), d[4])


def accept(flow_name: str, rating) -> bool:
    """Applies the given workflow recursively to the given rating

    flowname: name of the flow to follow, or A or R for a default verdict
    rating: the rating to apply the flow to

    returns: True iff the part is accepted"""

    # Default rules
    if flow_name in "AR":
        return flow_name == "A"

    # Skip the last: it will be a default value, without condition
    for rule in workflows[flow_name][:-1]:
        if rule[1] == "<" and rating[rule[0]] < rule[2]:
            return accept(rule[3], rating)
        if rule[1] == ">" and rating[rule[0]] > rule[2]:
            return accept(rule[3], rating)

    # Last entry is default
    return accept(workflows[flow_name][-1], rating)


with open("inputs/day19", "r") as f:
    flow_data, part_data = f.read().split("\n\n")

    ratings = [
        (int(a), int(b), int(c), int(d))
        for a, b, c, d in re.findall(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", part_data)
    ]
    workflows = {
        name: list(map(parse_rule_data, rules.split(",")))
        for name, rules in re.findall(r"([a-z]+)\{([^{}]*)\}", flow_data)
    }

# Part 1
part1 = sum(sum(rating) for rating in ratings if accept("in", rating))

# Part 2
accepted = 0
queue = Queue()
queue.put(("in", RangedRatings()))

while not queue.empty():
    flow_name, ratings = queue.get()

    if flow_name == "A":
        accepted += ratings.count()
    elif flow_name != "R":
        # Skip the last: it will be a default value, without condition
        for rule in workflows[flow_name][:-1]:
            lhs, cmp, rhs, nxt = rule
            if cmp == "<":
                lo, hi = ratings.split_below(lhs, rhs)
                if lo != None:
                    queue.put((nxt, lo))
                # Continue the current flow with the remaining ranges, break if we're out
                ratings = hi

            if cmp == ">":
                lo, hi = ratings.split_above(lhs, rhs)
                if hi != None:
                    queue.put((nxt, hi))
                # Continue the current flow with the remaining ranges, break if we're out
                ratings = lo

            if ratings == None:
                break

        if ratings != None:
            # Last rule is a default
            queue.put((workflows[flow_name][-1], ratings))

print(f"Part 1: {part1}")
print(f"Part 2: {accepted}")
