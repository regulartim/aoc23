import time

begin = time.time()

###

VERTICAL_PIPE_CHARS = set("|F7")
NEIGHBOURS = {
	"|": [(0,1), (0,-1)],
	"-": [(1,0), (-1,0)],
	"L": [(1,0), (0,-1)],
	"J": [(-1,0), (0,-1)],
	"7": [(-1,0), (0,1)],
	"F": [(1,0), (0,1)]
}

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def determinte_s_shape(m: dict, start: tuple) -> str:
	for shape, deltas in NEIGHBOURS.items():
		possible_neighbours = set(add_tuples(start, d) for d in deltas)
		if possible_neighbours == set(m[start]):
			return shape
	raise ValueError()

def get_loop(m: dict, start: tuple) -> set:
	loop = {start}
	adjacents = m[start]
	while adjacents:
		next_step = adjacents.pop()
		loop.add(next_step)
		adjacents = m[next_step] - loop
	return loop

def enclosed_area(loop: set, verticals: list) -> int:
	area, previous_x = 0, 0
	inside_loop = False
	for x, y in verticals:
		if inside_loop:
			area += sum(1 for i in range(previous_x, x) if (i, y) not in loop)
		previous_x = x
		inside_loop = not inside_loop
	return area


pipe_map = {}
vertical_pipes = set()
with open("input.txt") as file:
	for row_idx, line in enumerate(file.readlines()):
		for col_idx, char in enumerate(line):
			p = (col_idx, row_idx)
			if char == "S":
				starting_point = p
			if char in NEIGHBOURS:
				pipe_map[p] = set(add_tuples(p, n) for n in NEIGHBOURS[char])
			if char in VERTICAL_PIPE_CHARS:
				vertical_pipes.add(p)

pipe_map[starting_point] = [p for p, ns in pipe_map.items() if starting_point in ns]
starting_point_shape = determinte_s_shape(pipe_map, starting_point)
if starting_point_shape in VERTICAL_PIPE_CHARS:
	vertical_pipes.add(starting_point)

main_loop = get_loop(pipe_map, starting_point)
vertical_pipes_in_loop = vertical_pipes & set(main_loop)
sorted_verticals = sorted(vertical_pipes_in_loop, key=lambda tup: tup[::-1])
enclosed = enclosed_area(main_loop, sorted_verticals)

print(f"Part 1: {len(main_loop) // 2}")
print(f"Part 2: {enclosed}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
