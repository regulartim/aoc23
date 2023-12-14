import time

begin = time.time()

###

TARGET_CYCLE_COUNT = 1_000_000_000
DIRECTIONS = {
	"N": (0,-1),
	"W": (-1,0),
	"S": (0,1),
	"E": (1,0)
}

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def move_rocks(rocks: set, space: set, d: str) -> tuple:
	result, moved = set(), False
	for rock in rocks:
		next_pos = add_tuples(rock, DIRECTIONS[d])
		if next_pos not in space or next_pos in rocks:
			result.add(rock)
			continue
		result.add(next_pos)
		moved = True
	return (result, moved)

def tilt_platform(rocks: set, space: set, d: str) -> set:
	moved = True
	while moved:
		rocks, moved = move_rocks(rocks, space, d)
	return rocks

def perform_cycle(rocks: set, space: set) -> set:
	for direction in "NWSE":
		rocks = tilt_platform(rocks, space, direction)
	return rocks

def calculate_load(rocks: set, max_y: int) -> int:
	return sum(max_y+1-y for _, y in rocks)

def find_pattern(l: list) -> list:
	l = l[::-1]
	pattern = []
	for idx, elem in enumerate(l):
		pattern.append(elem)
		if pattern != l[idx+1:idx+1+len(pattern)]:
			continue
		return pattern[::-1]
	return []


round_rocks = set()
empty_space = set()
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		for col, char in enumerate(line.strip()):
			if char == "#":
				continue
			if char == "O":
				round_rocks.add((col, row))
			empty_space.add((col, row))
		y_dim = row

state_after_first_tilt = tilt_platform(round_rocks, empty_space, "N")

loads, reoccuring_pattern = [], []
while len(reoccuring_pattern) < 4:
	round_rocks = perform_cycle(round_rocks, empty_space)
	loads.append(calculate_load(round_rocks, y_dim))
	reoccuring_pattern = find_pattern(loads)

target_idx = (TARGET_CYCLE_COUNT-len(loads)) % len(reoccuring_pattern) - 1

print(f"Part 1: {calculate_load(state_after_first_tilt, y_dim)}")
print(f"Part 2: {reoccuring_pattern[target_idx]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
