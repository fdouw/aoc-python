with open("inputs/01") as f:
    total_calories = [
        sum(int(x) for x in calories.splitlines())
        for calories in f.read().split("\n\n")
    ]
print(f"Part 1: {max(total_calories)}")
print(f"Part 2: {sum(sorted(total_calories)[-3:])}")
