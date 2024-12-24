#!/usr/bin/env python


def compute(wire) -> int:
    if wire in inputs:
        return inputs[wire]

    a, f, b = tree[wire]

    if f == "AND":
        return compute(a) & compute(b)
    elif f == "XOR":
        return compute(a) ^ compute(b)
    elif f == "OR":
        return compute(a) | compute(b)
    else:
        raise f"Unknown operation: {f}"


with open("inputs/day24", "r") as f:
    in_data, conn_data = f.read().split("\n\n")

    # Read raw inputs
    inputs = dict()
    for l in in_data.splitlines():
        k, v = l.split(": ")
        inputs[k] = int(v)

    # Read the connectome
    tree = dict()
    outputs = list()
    for l in conn_data.splitlines():
        # "ntg XOR fgs -> mjb"
        a, f, b, _, c = l.split()
        tree[c] = (a, f, b)
        if c[0] == "z":
            outputs.append(c)

outputs.sort(reverse=True)
num = 0
for wire in outputs:
    bit = compute(wire)
    num = (num << 1) | bit

print(f"Part 1: {num} ({num:b})")
