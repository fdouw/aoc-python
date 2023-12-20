#!/usr/bin/env python

from collections import deque
from itertools import pairwise
from math import lcm


LO = False
HI = True


class ConjunctionModule:
    def __init__(self, name: str, output_str: str):
        self.name = name
        self.outputs = output_str.split(", ")
        self.memory = {}

    def process(self, source: str, signal: bool):
        self.memory[source] = signal
        out_signal = not all(self.memory.values())
        return ((self.name, next_module, out_signal) for next_module in self.outputs)

    def connect_input(self, input: str):
        self.memory[input] = False


class FlipFlopModule:
    def __init__(self, name: str, output_str: str):
        self.name = name
        self.outputs = output_str.split(", ")
        self.state = False

    def process(self, _source: str, signal: bool):
        if not signal:
            self.state = not self.state
            return (
                (self.name, next_module, self.state) for next_module in self.outputs
            )
        else:
            # Return empty list: caller expects something
            return ()

    def connect_input(self, input: str):
        pass


class BroadcastModule:
    def __init__(self, name: str, output_str: str):
        self.name = name
        self.outputs = output_str.split(", ")

    def process(self, _source: str, signal: bool):
        return ((self.name, next_module, signal) for next_module in self.outputs)

    def connect_input(self, input: str):
        pass


modules = {}

with open("inputs/day20", "r") as f:
    for line in f.readlines():
        module, dest = line.strip().split(" -> ")
        if module[0] == "&":
            modules[module[1:]] = ConjunctionModule(module[1:], dest)
        elif module[0] == "%":
            modules[module[1:]] = FlipFlopModule(module[1:], dest)
        elif module == "broadcaster":
            modules[module] = BroadcastModule(module, dest)
        else:
            raise f"Could not interpret module '{line}'"

# Make sure the Conjunctions know their inputs, quadratic unfortunately
rx_input = ""
for name, module in modules.items():
    for output in module.outputs:
        if output in modules:
            modules[output].connect_input(name)
        elif output == "rx":
            rx_input = name
            # print(f"direct input: {name}")

rx_inputs = {}
for name, module in modules.items():
    if rx_input in module.outputs:
        # print(f"input[{name}] = {modules[name]}")
        rx_inputs[name] = []


# Run the program
counts = [0, 0]
signal_queue = deque()

part2 = 0
for cycle in range(10_000):
    signal_queue.append(("button", "broadcaster", False))

    while signal_queue:
        source, dest, signal = signal_queue.popleft()
        if cycle < 1000:
            counts[signal] += 1
        if dest == "rx" and not signal:
            part2 = cycle
            break
        elif source in rx_inputs and signal is True:
            rx_inputs[source].append(cycle)
            if all(len(x) >= 2 for x in rx_inputs.values()):
                # Assume there are cycles
                break

        if dest in modules:
            for new_signal in modules[dest].process(source, signal):
                signal_queue.append(new_signal)

part1 = counts[0] * counts[1]

# for name, hist in rx_inputs.items():
#     print(f"{name}: {hist[:20]} -- {[b-a for a,b in pairwise(hist[:20])]}")

part2 = lcm(*[hist[1] - hist[0] for hist in rx_inputs.values()])


print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
