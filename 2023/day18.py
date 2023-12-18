#!/usr/bin/env python


from queue import Queue


dirs = (0 - 1j, 0 + 1j, -1 + 0j, 1 + 0j)


# def print_dig(labels=True):
#     if labels:
#         print(" ", end="")
#         print("".join(str(x % 10) for x in range(min_x, max_x + 1)))
#     for y in range(min_y, max_y + 1):
#         if labels:
#             print(y % 10, end="")
#         for x in range(min_x, max_x + 1):
#             z = complex(x, y)
#             if z in dig:
#                 print("#", end="")
#             elif z in outside:
#                 print("O", end="")
#             else:
#                 print(".", end="")
#         if labels:
#             print(y % 10)
#     if labels:
#         print(" ", end="")
#         print("".join(str(x % 10) for x in range(min_x, max_x + 1)))
#     print()


with open("inputs/day18", "r") as f:
    dig = set()
    position = 0 + 0j
    for line in f.readlines():
        direction, distance, hex = line.split()
        step = dirs["UDLR".index(direction)]
        for _ in range(int(distance)):
            position += step
            dig.add(position)


def measure_inside(dig: set[complex]) -> int:
    # Take a boundary of 1m around the min and max x and y, this boundary is definitely outside the loop and also
    # guarantees that all the outside areas are connected(?) Then do a flood fill to determine the area outside the loop
    x_vals = set(int(z.real) for z in dig)
    y_vals = set(int(z.imag) for z in dig)
    min_x = min(x_vals) - 1
    max_x = max(x_vals) + 2  # max is 1 more, because half open ranges
    min_y = min(y_vals) - 1
    max_y = max(y_vals) + 2  # idem
    total_area = (max_x - min_x) * (max_y - min_y)

    seen = set()
    outside = 0
    queue = Queue()
    queue.put(complex(min_x, min_y))
    seen.add(complex(min_x, min_y))

    while not queue.empty():
        item = queue.get()
        outside += 1
        for step in dirs:
            nb = item + step
            if (
                nb not in seen
                and nb not in dig
                and min_x <= nb.real < max_x
                and min_y <= nb.imag < max_y
            ):
                queue.put(nb)
            seen.add(nb)

    return total_area - outside


print(f"Part 1: {measure_inside(dig)}")
