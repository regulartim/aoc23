import time

begin = time.time()

###

DIRECTIONS = {"R": (1,0), "D": (0,1), "L": (-1,0), "U": (0,-1)}
NUMBER_TO_DIR = list(DIRECTIONS)

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def scale_tuple(t: tuple, factor: int) -> tuple:
	return tuple(factor * n for n in t)

def color_code_to_instruction(color: str) -> tuple:
	distance, direction = color[:-1], int(color[-1])
	return (NUMBER_TO_DIR[direction], int(distance, 16))

def dig_trench(plan: list) -> list:
	result = [(0,0)]
	for d, meters in plan:
		delta = scale_tuple(DIRECTIONS[d], meters)
		result.append(add_tuples(result[-1], delta))
	return result

def polygon_area(loop: list) -> int:
	""" Shoelace formula """
	area = 0
	for a, b in zip(loop, loop[1:] + [loop[0]]):
		area += a[0] * b[1]
		area -= a[1] * b[0]
	return abs(area) // 2


dig_plan_p1, dig_plan_p2 = [], []
with open("input.txt") as file:
	for line in file.readlines():
		line = line.strip().split()
		p1_line = line[0], int(line[1])
		p2_line = color_code_to_instruction(line[2][2:-1])
		dig_plan_p1.append(p1_line)
		dig_plan_p2.append(p2_line)

lagoon_volumes = []
for dig_plan in [dig_plan_p1, dig_plan_p2]:
	trench = dig_trench(dig_plan)
	trench_length = sum(line[1] for line in dig_plan)
	lagoon_volumes += [polygon_area(trench) - trench_length//2 + trench_length + 1] # Pick's theorem

print(f"Part 1: {lagoon_volumes[0]}")
print(f"Part 2: {lagoon_volumes[1]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
