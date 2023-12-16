import time
from functools import cache

begin = time.time()

###

DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]
TURNS ={"/": [-1, 1, -1, 1], "\\": [1, -1, 1, -1]}

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

@cache
def get_next_states(point: tuple, dir_idx: int, tile: str) -> list:
	if tile == "." or tile == "-|"[dir_idx%2]:
		return [(*add_tuples(point, DIRECTIONS[dir_idx]), dir_idx)]
	if tile in "\\/":
		turn = TURNS[tile][dir_idx]
		dir_idx = (dir_idx + turn) % 4
		return [(*add_tuples(point, DIRECTIONS[dir_idx]), dir_idx)]
	if tile in "-|":
		d1, d2 = (dir_idx + 1) % 4, (dir_idx - 1) % 4
		return [(*add_tuples(point, DIRECTIONS[d1]), d1),
				(*add_tuples(point, DIRECTIONS[d2]), d2)]
	return []

def energized_tiles(grid: dict, start: tuple) -> set:
	seen = set()
	stack = [start]
	while stack:
		current = stack.pop()
		point, dir_idx = current[:2], current[-1]
		if current in seen:
			continue
		if point not in grid:
			continue
		seen.add(current)
		stack += get_next_states(point, dir_idx, grid[point])
	return {(x,y) for x, y, dir_idx in seen}


contraption_grid = {}
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		max_y = row
		for  col, char in enumerate(line.strip()):
			max_x = col
			contraption_grid[(col, row)] = char

starting_points = [(0, y, 0) for y in range(max_y)] \
 				+ [(max_x, y, 2) for y in range(max_y)] \
				+ [(x, 0, 1) for x in range(max_x)] \
				+ [(x, max_y, 3) for x in range(max_x)]
tile_counts = [len(energized_tiles(contraption_grid, s)) for s in starting_points]

print(f"Part 1: {len(energized_tiles(contraption_grid, (0,0,0)))}")
print(f"Part 2: {max(tile_counts)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
