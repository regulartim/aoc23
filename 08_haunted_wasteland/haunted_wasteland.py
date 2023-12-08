import re
import time
from math import lcm

begin = time.time()

###

def count_steps(start: str, finish: str, nodes: dict, instrs: list) -> int:
	current = start
	instr_idx = 0
	step_counter = 0
	while not current.endswith(finish):
		instr = instrs[instr_idx]
		current = nodes[current][instr]
		instr_idx = (instr_idx + 1) % len(instrs)
		step_counter += 1
	return step_counter


with open("input.txt") as file:
	instruction_block, node_block = file.read().split("\n\n")

instructions = [0 if instr == "L" else 1 for instr in instruction_block]
node_map = [re.findall(r"\w+", node) for node in node_block.splitlines()]
node_map = {key: tuple(values) for key, *values in node_map}

p1_count = count_steps("AAA", "ZZZ", node_map, instructions)
start_nodes = [node for node in node_map if node.endswith("A")]
p2_count = lcm(*[count_steps(node, "Z", node_map, instructions) for node in start_nodes])

print(f"Part 1: {p1_count}")
print(f"Part 2: {p2_count}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
