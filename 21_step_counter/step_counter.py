import time
from collections import deque

begin = time.time()

###

STEPS_TO_GO = (64, 26501365)

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def shortest_paths(start: tuple, grid: set) -> dict:
	result = {}
	q = deque([(0, start)])
	while q:
		dist, current = q.popleft()
		if current not in grid:
			continue
		if current in result:
			continue
		result[current] = dist
		for delta in [(0,1), (1,0), (-1,0), (0,-1)]:
			n = add_tuples(current, delta)
			q.append((dist+1, n))
	return result

def estimate_reachable_plots(steps: int, start: tuple, distances: dict) -> int:
	grid_dimensions = max(distances.keys())
	assert start[0] == start [1]
	assert grid_dimensions[0] == grid_dimensions[1]
	assert 2 * start[0] == grid_dimensions[0]

	middle = start[0]
	grid_diameter = grid_dimensions[0] + 1
	assert (steps - middle) % grid_diameter == 0
	n = (steps - middle) // grid_diameter
	assert n % 2 == 0

	inners = [dist for dist in distances.values() if dist <= middle]
	outers = [dist for dist in distances.values() if dist > middle]
	evens        = sum(1 for dist in distances.values() if dist % 2 == 0)
	odds         = sum(1 for dist in distances.values() if dist % 2 == 1)
	inner_evens  = sum(1 for dist in inners if dist % 2 == 0)
	inner_odds   = sum(1 for dist in inners if dist % 2 == 1)
	outer_evens  = sum(1 for dist in outers if dist % 2 == 0)
	outer_odds   = sum(1 for dist in outers if dist % 2 == 1)

	assert len(inners) + len(outers) == len(distances)
	assert evens + odds == len(distances)
	assert inner_evens + outer_evens == evens
	assert inner_odds + outer_odds == odds

	result  = n**2 * evens
	result += (n-1)**2 * odds
	result += n * outer_evens
	result += 4 * n * inner_odds
	result += 3 * (n-1) * outer_odds
	result += 2 * outer_odds
	return result


garden_map = set()
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		for  col, char in enumerate(line.strip()):
			if char == "#":
				continue
			if char == "S":
				starting_point = (col, row)
			garden_map.add((col, row))

distances_to_start = shortest_paths(starting_point, garden_map)
p1_plots = [p for p, dist in distances_to_start.items()
						if dist <= STEPS_TO_GO[0] and dist % 2 == STEPS_TO_GO[0] % 2]
p2_plot_count = estimate_reachable_plots(STEPS_TO_GO[1], starting_point, distances_to_start)

print(f"Part 1: {len(p1_plots)}")
print(f"Part 2: {p2_plot_count}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
