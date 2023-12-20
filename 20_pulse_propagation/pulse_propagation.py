import time
from collections import deque
from math import lcm

begin = time.time()

###

class Module:
	def __init__(self, name: str, outputs: list) -> None:
		self.name = name[1:] if name[0] in "%&" else name
		self.typ = name[0] if name[0] in "%&" else name
		self.inputs = {}
		self.outputs = outputs
		self.state = False

	def __repr__(self) -> str:
		return self.name

	def receive(self, sender: str, pulse: bool) -> list:
		match self.typ:
			case "broadcaster":
				return [(self.name, pulse, o) for o in self.outputs]
			case "%":
				if pulse:
					return []
				self.state = not self.state
				return [(self.name, self.state, o) for o in self.outputs]
			case "&":
				self.inputs[sender] = pulse
				out_pulse = not all(self.inputs.values())
				return [(self.name, out_pulse, o) for o in self.outputs]
		return []


def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def perform_sequence(modules: dict, monitored: list) -> int:
	counter, found = [0,0], None
	q = deque()
	q.append(["button", False, "broadcaster"])
	while q:
		sender, pulse, receiver = q.popleft()
		counter[pulse] += 1
		q.extend(modules[receiver].receive(sender, pulse))
		if receiver in monitored and not pulse:
			found = receiver
	return tuple(counter), found

def push_button(modules: dict, n_times: int, monitored: list) -> int:
	total_count, pulse_count_product = (0,0), 0
	cycle_lengths = {}
	sequence_count = 0
	while len(cycle_lengths) < len(monitored):
		sequence_count += 1
		counter, found = perform_sequence(modules, monitored)
		total_count = add_tuples(counter, total_count)
		if sequence_count == n_times:
			pulse_count_product = total_count[0] * total_count[1]
		if found and found not in cycle_lengths:
			cycle_lengths[found] = sequence_count
	return pulse_count_product, lcm(*list(cycle_lengths.values()))


com_modules = {}
with open("input.txt") as file:
	for line in file.readlines():
		mod_name, outs = line.split("->")
		outs = [o.strip() for o in outs.split(",")]
		m = Module(name=mod_name.strip(), outputs=outs)
		com_modules[m.name] = m

com_modules["rx"] = Module(name="rx", outputs=[])

for mod_name, mod in com_modules.items():
	for other in mod.outputs:
		com_modules[other].inputs[mod_name] = False

assert len(com_modules["rx"].inputs) == 1
rx_predecessor = next(iter(com_modules["rx"].inputs))
rx_prepredecessors = list(com_modules[rx_predecessor].inputs.keys())

p1_result, p2_result = push_button(com_modules, 1000, rx_prepredecessors)

print(f"Part 1: {p1_result}")
print(f"Part 2: {p2_result}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
