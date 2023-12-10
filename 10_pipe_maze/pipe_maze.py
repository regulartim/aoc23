import time

begin = time.time()

###

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

def get_loop(m: dict, start: tuple) -> set:
	seen = {start}
	loop = [start]
	adjacents = m[start]
	while adjacents:
		next_step = adjacents.pop()
		seen.add(next_step)
		loop.append(next_step)
		adjacents = m[next_step] - seen
	return loop

def polygon_area(loop: list) -> int:
	""" Shoelace formula """
	area = 0
	for a, b in zip(loop, loop[1:] + [loop[0]]):
		area += a[0] * b[1]
		area -= a[1] * b[0]
	return abs(area) // 2


pipe_map = {}
with open("input.txt") as file:
	for y, line in enumerate(file.readlines()):
		for x, char in enumerate(line):
			p = (x, y)
			if char == "S":
				starting_point = p
			if char in NEIGHBOURS:
				pipe_map[p] = set(add_tuples(p, n) for n in NEIGHBOURS[char])

pipe_map[starting_point] = [p for p, ns in pipe_map.items() if starting_point in ns]
main_loop = get_loop(pipe_map, starting_point)
area_inside_loop = polygon_area(main_loop)
enclosed_tile_count = area_inside_loop - len(main_loop)//2 + 1 # Pick's theorem

print(f"Part 1: {len(main_loop) // 2}")
print(f"Part 2: {enclosed_tile_count}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
