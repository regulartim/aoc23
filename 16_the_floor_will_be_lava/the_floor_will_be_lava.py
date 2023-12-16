import time
from functools import cache

begin = time.time()

###

DIRECTIONS = [(-1,0), (0,-1), (1,0), (0,1)]
TURNS ={"/": [-1, 1, -1, 1], "\\": [1, -1, 1, -1]}

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

@cache
def get_next_states(x: int, y: int, d: int, tile: str) -> list:
	if tile == "." or tile == "-|"[d%2]:
		return [(*add_tuples((x,y), DIRECTIONS[d]), d)]
	if tile in "\\/":
		turn = TURNS[tile][d]
		d = (d + turn) % 4
		return [(*add_tuples((x,y), DIRECTIONS[d]), d)]
	if tile in "-|":
		d1, d2 = (d + 1) % 4, (d - 1) % 4
		return [(*add_tuples((x,y), DIRECTIONS[d1]), d1),
				(*add_tuples((x,y), DIRECTIONS[d2]), d2)]
	return []

def energized_tiles(grid: dict, start: tuple) -> list:
	seen = set()
	q = [start]
	while q:
		current = q.pop()
		x, y, d = current
		if current in seen:
			continue
		if (x,y) not in grid:
			continue
		seen.add(current)
		q += get_next_states(x, y, d, grid[(x,y)])
	return list(set((x,y) for x,y,d in seen))


contraption_grid = {}
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		max_y = row
		for  col, char in enumerate(line.strip()):
			max_x = col
			contraption_grid[(col, row)] = char

starting_points = [(0, y, 2) for y in range(max_y)]
starting_points += [(max_x, y, 0) for y in range(max_y)]
starting_points += [(x, 0, 3) for x in range(max_x)]
starting_points += [(x, max_y, 1) for x in range(max_x)]
tile_counts = [len(energized_tiles(contraption_grid, s)) for s in starting_points]

print(f"Part 1: {len(energized_tiles(contraption_grid, (0,0,2)))}")
print(f"Part 2: {max(tile_counts)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
