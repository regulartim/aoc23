import time
from itertools import combinations

begin = time.time()

###

def manhattan_distance(s: tuple, t: tuple) -> int:
	return sum(abs(a - b) for a, b in zip(s, t))

def expand_map(m: set, factor: int) -> set:
	max_x, _ = max(m)
	_, max_y = max(m, key=lambda tup: tup[1])
	col_occupation = [False for _ in range(max_x + 1)]
	row_occupation = [False for _ in range(max_y + 1)]
	for x, y in m:
		col_occupation[x] = True
		row_occupation[y] = True
	result = set()
	for x, y in m:
		new_x = sum(col_occupation[:x]) + factor * (x - sum(col_occupation[:x]))
		new_y = sum(row_occupation[:y]) + factor * (y - sum(row_occupation[:y]))
		result.add((new_x, new_y))
	return result


galaxy_map = set()
with open("input.txt") as file:
	for y_idx, line in enumerate(file.readlines()):
		for x_idx, char in enumerate(line):
			if char == "#":
				galaxy_map.add((x_idx, y_idx))

p1_map = expand_map(galaxy_map, 2)
p1_distances = [manhattan_distance(a, b) for a, b in combinations(p1_map, 2)]
p2_map = expand_map(galaxy_map, 1_000_000)
p2_distances = [manhattan_distance(a, b) for a, b in combinations(p2_map, 2)]

print(f"Part 1: {sum(p1_distances)}")
print(f"Part 2: {sum(p2_distances)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
