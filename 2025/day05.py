#!/usr/bin/env python


def combine(ranges: list[list[int]], item: list[int]):
    follow_up = None
    for r in ranges:
        if item[0] >= r[0] and item[1] <= r[1]:
            # identical ranges, or the new item is inside an existing range; ignore the new one (ie return without altering ranges)
            return
        elif item[0] <= r[0]:
            if item[1] < r[0]:
                # new item is to the left of this one
                continue
            elif item[1] <= r[1]:
                # expand to the left only
                r[0] = item[0]
                follow_up = r
                break
            elif item[1] > r[1]:
                # expand both ways
                r[0] = item[0]
                r[1] = item[1]
                follow_up = r
                break
        elif item[0] <= r[1]:
            if item[1] <= r[1]:
                continue
            else:
                # item[1] > r[1], and item[0] > r[0], so overlapping to the right
                r[1] = item[1]
                follow_up = r
                break
    if follow_up:
        # print(f"Follow up: {ranges=}\t{follow_up=}")
        ranges.remove(follow_up)
        combine(ranges, follow_up)
    else:
        # print(f"Append ranges: {ranges=}\t{item=}")
        ranges.append(item)


with open("inputs/05.txt") as f:
    range_data, id_data = f.read().split("\n\n")

    ranges = [list(map(int, l.split("-"))) for l in range_data.splitlines()]
    clean_ranges = []
    for r in ranges:
        combine(clean_ranges, r)

    part1 = sum(any(item >= r[0] and item <= r[1] for r in clean_ranges) for item in map(int, id_data.splitlines()))
    total_ids = sum(r[1] + 1 - r[0] for r in clean_ranges)


print(f"Part 1: {part1}")
print(f"Part 2: {total_ids}")
