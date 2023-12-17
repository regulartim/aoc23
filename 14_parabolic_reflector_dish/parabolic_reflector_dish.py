import time
from functools import cache

begin = time.time()

###

TARGET_CYCLE_COUNT = 1_000_000_000

def rotate_clockwise(grid: list, x_times=1) -> list:
	for _ in range(x_times):
		grid = ["".join(reversed(column)) for column in zip(*grid)]
	return grid

@cache
def move_rocks_left(row: str) -> str:
	results = []
	for section in row.split("#"):
		rock_count = section.count("O")
		space_count = len(section) - rock_count
		results.append("O" * rock_count + "." * space_count)
	return "#".join(results)

def perform_cycle(grid: list) -> list:
	for _ in range(4):
		grid = [move_rocks_left(row) for row in grid]
		grid = rotate_clockwise(grid)
	return grid

def calculate_load(grid: list) -> int:
	max_load_per_rock = len(grid[0])
	column_loads = [(max_load_per_rock - idx) * col.count("O") for idx, col in enumerate(zip(*grid))]
	return sum(column_loads)

def find_pattern(loads: list) -> list:
	loads = loads[::-1]
	pattern = []
	for idx, load in enumerate(loads):
		pattern.append(load)
		if pattern != loads[idx+1:idx+1+len(pattern)]:
			continue
		return pattern[::-1]
	return []


with open("input.txt") as file:
	rock_grid = [line.strip() for line in file.readlines()]

rock_grid = rotate_clockwise(rock_grid, 3) # such that north is on the left side of the grid
state_after_first_tilt = [move_rocks_left(row) for row in rock_grid]

recorded_loads, reoccuring_pattern = [], []
while len(reoccuring_pattern) < 4:
	rock_grid = perform_cycle(rock_grid)
	recorded_loads.append(calculate_load(rock_grid))
	reoccuring_pattern = find_pattern(recorded_loads)

target_idx = (TARGET_CYCLE_COUNT-len(recorded_loads)) % len(reoccuring_pattern) - 1

print(f"Part 1: {calculate_load(state_after_first_tilt)}")
print(f"Part 2: {reoccuring_pattern[target_idx]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
