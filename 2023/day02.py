#!/usr/bin/env python

test_data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


part1 = 0
part2 = 0
with open("inputs/day02") as f:
    for line in f.readlines():
        # for line in test_data.splitlines():
        game, draws = line.strip().replace(" ", "").split(":")
        red = green = blue = 0
        for draw in draws.split(";"):
            for colour in draw.split(","):
                if colour.endswith("red"):
                    red = max(red, int(colour[:-3]))
                elif colour.endswith("green"):
                    green = max(green, int(colour[:-5]))
                elif colour.endswith("blue"):
                    blue = max(blue, int(colour[:-4]))
        part2 += red * green * blue
        if red <= 12 and green <= 13 and blue <= 14:
            part1 += int(game[4:])

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
