#!/usr/bin/env python

# inputs/day05_test2 p2 => 6082852


class mapper:
    def __init__(self, name=""):
        self.name = name
        self.table = []

    def add_rule(self, line: str):
        # dest, src, len => src_start, src_end, delta
        dest, src, len = map(int, line.split(" "))
        src_start = src
        src_end = src + len
        diff = dest - src
        self.table.append((src_start, src_end, diff))

    def sort(self):
        self.table = sorted(self.table)

    def lookup(self, n: int) -> int:
        for rule in self.table:
            if rule[0] <= n < rule[1]:
                return n + rule[2]
        return n

    def lookup_range(self, a: int, b: int):
        assert a < b
        res = []
        for rule in self.table:
            assert a < b
            if rule[0] <= a and b <= rule[1]:
                res.append([a + rule[2], b + rule[2]])
                a = b
            elif rule[0] <= a < rule[1]:
                res.append([a + rule[2], rule[1] + rule[2]])
                a = rule[1]
            elif rule[0] < b <= rule[1]:
                res.append([rule[0] + rule[2], b + rule[2]])
                b = rule[0]
            if a == b:
                break
        if a < b:
            res.append([a, b])
        return res

    def lookup_range_list(self, ranges):
        res = []
        for range in ranges:
            res.extend(self.lookup_range(range[0], range[1]))
        return res


with open("inputs/day05", "r") as f:
    seed_list = list(map(int, f.readline().split(":")[1].strip().split(" ")))

    # Read maps
    table_list = []
    for line in f.readlines():
        line = line.strip()
        if line == "":
            continue
        elif line.endswith("map:"):
            name = line.split(" ")[0]
            table_list.append(mapper(name))
        else:
            table_list[-1].add_rule(line)
    for table in table_list:
        table.sort()

    # Part 1
    location = 10_000_000_000
    for seed in seed_list:
        cur = seed
        for table in table_list:
            cur = table.lookup(cur)
        location = min(location, cur)

    # Part 2
    ranges = [
        [seed_list[i], seed_list[i] + seed_list[i + 1]]
        for i in range(0, len(seed_list), 2)
    ]

    for table in table_list:
        ranges = table.lookup_range_list(ranges)

    part2 = min(ranges, key=lambda x: x[0])[0]


print(f"Part 1: {location}")
print(f"Part 2: {part2}")
