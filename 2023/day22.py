#!/usr/bin/env python


class Brick:
    def __init__(self, line: str):
        a, b = line.strip().split("~")
        a = tuple(map(int, a.split(",")))
        b = tuple(map(int, b.split(",")))
        self.x = (min(a[0], b[0]), max(a[0], b[0]))
        self.y = (min(a[1], b[1]), max(a[1], b[1]))
        self.z = (min(a[2], b[2]), max(a[2], b[2]))

        # Keep track of bricks directly above and below (ie which are supported by this brick and which are supporting this brick)
        self.below = set()
        self.above = set()

    def is_below(self, other):
        """Returns True iff self and other overlap in the x-y plane and self is below other along the z-axis."""
        return (
            (self.x[0] <= other.x[1] and other.x[0] <= self.x[1])
            and (self.y[0] <= other.y[1] and other.y[0] <= self.y[1])
            and (self.z[1] <= other.z[0])
        )

    def drop(self, newz: int):
        """Drops this brick down so the new lower z-value is newz. No checking is done for collisions."""
        len = self.z[1] - self.z[0]
        self.z = (newz, newz + len)

    def collapse(self):
        """Checks if the current brick is supported by a subset of <removed>. If so, add this brick to remove and all
        bricks above it that would fall (check recursively)."""
        removed = {self}
        for other in self.above:
            other._collapse(removed)
        removed.remove(self)
        return removed

    def _collapse(self, removed):
        if self.below.issubset(removed):
            removed.add(self)
            for other in self.above:
                other._collapse(removed)


with open("inputs/day22", "r") as f:
    bricks = [Brick(line) for line in f.readlines()]

# Keep bricks sorted by z-value, also, after settling, keep track of the bricks by lower z-value, to keep track of neighbours
bricks.sort(key=lambda v: v.z[0])
by_zval = [[] for _ in range(bricks[-1].z[0])]

# Adding the floor for bricks to land on; needed below to find the z-val
base = Brick("0,0,0~1000,1000,0")
settled = [base]
for brick in bricks:
    # compare to settled bricks, put it in lowest place possible and add to settled
    # Start by getting the highest z-value for the x,y footprint of brick
    top_z = max((other.z[1] for other in settled if other.is_below(brick)))
    brick.drop(top_z + 1)
    settled.append(brick)
    by_zval[top_z + 1].append(brick)

# For each brick, find the bricks that it supports
for brick in bricks:
    for other in by_zval[brick.z[1] + 1]:
        if brick.is_below(other):
            other.below.add(brick)
            brick.above.add(other)

remove_count = 0
chain_count = 0
for brick in bricks:
    if len(brick.above) == 0 or all(len(other.below) > 1 for other in brick.above):
        # Each brick supported by the current brick is also supported by yet others
        # Therefor we can safely remove this one
        remove_count += 1
    else:
        supported = brick.collapse()
        chain_count += len(supported)


print(f"Part 1: {remove_count}")
print(f"Part 2: {chain_count}")
