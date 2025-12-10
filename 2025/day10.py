#!/usr/bin/env python

from collections import deque
from pprint import pprint
import re

machine_pattern = re.compile(r"\[(.+)\] (.+) \{(.+)\}")


class Machine:

    def from_str(data: str):
        results = machine_pattern.match(data)
        target = [c == "#" for c in results.group(1)]  # How the indicator lights should look
        lights = [False] * len(target)  # The indicator lights
        buttons = []  # How the buttons are wired (which lights flip)
        for tuple in results.group(2).split():
            buttons.append([int(c) for c in tuple.strip("()").split(",")])
        press_count = 0  # How often we've pressed a button to get to this state
        # Ignore curly braces for now
        return Machine(target, lights, buttons, press_count)

    def __init__(self, target, lights, buttons, press_count=0):
        self.target = target
        self.lights = lights
        self.buttons = buttons
        self.press_count = press_count

    def __str__(self):
        lights = "".join("#" if l else "." for l in self.lights)
        target = "".join("#" if l else "." for l in self.target)
        buttons = " ".join(map(str, self.buttons))
        return f"[{target}] {buttons} -> [{lights}] (presses: {self.press_count})"

    def press_buttons(self):
        for button in self.buttons:
            lights = self.lights.copy()
            for b in button:
                lights[b] = not lights[b]
            yield Machine(self.target, lights, self.buttons, self.press_count + 1)


with open("inputs/10.txt") as f:
    machines = [Machine.from_str(line) for line in f.readlines()]

    total_presses = 0
    for machine in machines:
        queue = deque([machine])
        while queue:
            m = queue.popleft()
            if m.lights == m.target:
                print(m.press_count)
                total_presses += m.press_count
                break
            else:
                queue.extend(m.press_buttons())

print(f"Part 1: {total_presses}")
