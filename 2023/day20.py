#!/usr/bin/env python

from queue import Queue


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
        return [(self.name, next_module, out_signal) for next_module in self.outputs]

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
            return [
                (self.name, next_module, self.state) for next_module in self.outputs
            ]
        else:
            # Return empty list: caller expects something
            return []

    def connect_input(self, input: str):
        pass


class BroadcastModule:
    def __init__(self, name: str, output_str: str):
        self.name = name
        self.outputs = output_str.split(", ")

    def process(self, _source: str, signal: bool):
        return [(self.name, next_module, signal) for next_module in self.outputs]

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
for name, module in modules.items():
    for output in module.outputs:
        if output in modules:
            modules[output].connect_input(name)

# Run the program
counts = [0, 0]
signal_queue = Queue()

part2 = 0
for cycle in range(1_000_000_000):
    signal_queue.put(("button", "broadcaster", False))

    while not signal_queue.empty():
        source, dest, signal = signal_queue.get()
        # print(f"{source} -{signal}-> {dest}")
        if cycle < 1000:
            counts[signal] += 1
        if dest == "rx" and not signal:
            part2 = cycle

        if dest in modules:
            for new_signal in modules[dest].process(source, signal):
                signal_queue.put(new_signal)

    if cycle >= 1000 and part2 > 0:
        break

part1 = counts[0] * counts[1]

print(f"Part 1: {part1}")
