#!/usr/bin/env python


from collections import defaultdict
from pprint import pprint


with open("inputs/day05", "r") as f:
    rule_data, page_data = f.read().split("\n\n")


rules = defaultdict(set)
for rd in rule_data.splitlines():
    k, v = map(int, rd.split("|"))
    rules[k].add(v)

part1 = 0
part2 = 0
for ordering in page_data.splitlines():
    previous = set()
    pages = list(map(int, ordering.split(",")))
    in_order = True
    for page in pages:
        if rules[page].isdisjoint(previous):
            previous.add(page)
        else:
            in_order = False
            break
    if in_order:
        part1 += pages[len(pages) // 2]
    else:
        all_pages = set(pages)
        predecessors = {p: all_pages.difference({p}, rules[p]) for p in pages}
        # pprint(f"{predecessors = }")
        ordered = list()
        while predecessors:
            for k, v in predecessors.items():
                if not v:
                    # predecessors is empty, this one goes first
                    ordered.append(k)
                    break
            # This assumes there alsways is an empty predecessor set
            predecessors.pop(ordered[-1])
            for v in predecessors.values():
                v.discard(ordered[-1])
        part2 += ordered[len(ordered) // 2]


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
