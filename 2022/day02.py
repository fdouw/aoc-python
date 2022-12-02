part1 = part2 = 0
with open("inputs/02") as f:
    for line in f.readlines():
        if line == "A X\n":
            part1 += 3 + 1
            part2 += 0 + 3
        elif line == "A Y\n":
            part1 += 6 + 2
            part2 += 3 + 1
        elif line == "A Z\n":
            part1 += 0 + 3
            part2 += 6 + 2
        elif line == "B X\n":
            part1 += 0 + 1
            part2 += 0 + 1
        elif line == "B Y\n":
            part1 += 3 + 2
            part2 += 3 + 2
        elif line == "B Z\n":
            part1 += 6 + 3
            part2 += 6 + 3
        elif line == "C X\n":
            part1 += 6 + 1
            part2 += 0 + 2
        elif line == "C Y\n":
            part1 += 0 + 2
            part2 += 3 + 3
        elif line == "C Z\n":
            part1 += 3 + 3
            part2 += 6 + 1
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
