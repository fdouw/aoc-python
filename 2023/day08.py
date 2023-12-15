#!/usr/bin/env python

from functools import reduce
from math import lcm

####


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


##########


def combine_periodics(a: (int, int), b: (int, int)) -> (int, int):
    """Combine two phased rotations into a single combined phased rotation

    Returns: combined_period, combined_phase

    Reference: https://math.stackexchange.com/a/3864593"""
    gcd, s, _ = extended_gcd(a[0], b[0])
    phase_difference = b[1] - a[1]
    combined_period = lcm(a[0], b[0])
    combined_phase = (phase_difference * s * a[0] // gcd + a[1]) % combined_period
    return (combined_period, combined_phase)


with open("inputs/day08", "r") as f:
    instructions, node_data = f.read().split("\n\n")
    instructions = [x == "R" for x in instructions]
    network = {}
    for line in node_data.splitlines(False):
        name, target_data = line.split(" = ")
        targets = target_data.strip("()").split(", ")
        network[name] = [targets[0], targets[1], 0, 0]

    # Part 1
    pos = "AAA"
    steps = 0
    while pos != "ZZZ":
        pos = network[pos][instructions[steps % len(instructions)]]
        steps += 1
    part1 = steps

    # Part 2
    start_nodes = set(filter(lambda n: n.endswith("A"), network.keys()))
    end_nodes = set(filter(lambda n: n.endswith("Z"), network.keys()))

    positions = list(start_nodes)
    phases = [0] * len(positions)
    periods = [0] * len(positions)
    for i, cur_start in enumerate(positions):
        # First determine phase by finding the end node
        pos = network[cur_start][instructions[0]]
        step = 1
        while pos not in end_nodes:
            pos = network[pos][instructions[step % len(instructions)]]
            step += 1
        phases[i] = step

        # Then determine period by finding the node again
        pos = network[pos][instructions[step % len(instructions)]]
        step += 1
        while pos not in end_nodes:
            pos = network[pos][instructions[step % len(instructions)]]
            step += 1
        periods[i] = step - phases[i]

    period, _phase = reduce(combine_periodics, zip(periods, phases))
    part2 = period


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
