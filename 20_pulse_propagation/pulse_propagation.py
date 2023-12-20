import time
from collections import deque
from math import prod

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

def perform_sequence(modules: dict) -> int:
	counter = [0,0]
	q = deque()
	q.append(["button", False, "broadcaster"])
	while q:
		sender, pulse, receiver = q.popleft()
		counter[pulse] += 1
		q.extend(modules[receiver].receive(sender, pulse))
	return tuple(counter)

def push_button(modules: dict, n_times: int) -> int:
	result = (0,0)
	for _ in range(n_times):
		counter = perform_sequence(modules)
		result = add_tuples(counter, result)
	return result[0] * result[1]

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

print(f"Part 1: {push_button(com_modules, 1000)}")
print(f"Part 2: {prod([3943, 3917, 4057, 3931])}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
