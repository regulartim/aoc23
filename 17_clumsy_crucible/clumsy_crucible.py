import heapq
import time

begin = time.time()

###

DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

def neighbours(valid_coords: frozenset, p: tuple, dir_idx: int) -> tuple:
	result = []
	for dir_delta in [0,-1,1]:
		new_dir = (dir_idx + dir_delta) % 4
		new_p = add_tuples(p, DIRECTIONS[new_dir])
		if new_p not in valid_coords:
			continue
		result.append((dir_delta != 0, new_p, new_dir))
	return tuple(result)

def shortest_path(grid: dict, start: tuple, target: tuple, movement_interval: tuple) -> int:
	min_move, max_move = movement_interval
	valid_coords = frozenset(grid)
	q = [(0, start, dir_idx, 0) for dir_idx in range(4)]
	seen = set()
	while q:
		dist, p, dir_idx, dir_count = heapq.heappop(q)
		if p == target:
			if dir_count < min_move:
				continue
			return dist
		if (p, dir_idx, dir_count) in seen:
			continue
		seen.add((p, dir_idx, dir_count))
		for turn, new_p, new_dir in neighbours(valid_coords, p, dir_idx):
			if turn and dir_count < min_move:
				continue
			if not turn and dir_count == max_move:
				continue
			new_dir_count = 1 if turn else dir_count + 1
			if (new_p, new_dir, new_dir_count) in seen:
				continue
			heapq.heappush(q, (dist + grid[new_p], new_p, new_dir, new_dir_count))
	return -1


heat_loss_map = {}
with open("input.txt") as file:
	for row, line in enumerate(file.readlines()):
		max_y = row
		for  col, n in enumerate(line.strip()):
			max_x = col
			heat_loss_map[(col, row)] = int(n)

start_pos, target_pos = (0, 0), (max_x, max_y)
print(f"Part 1: {shortest_path(heat_loss_map, start_pos, target_pos, movement_interval=(0, 3))}")
print(f"Part 2: {shortest_path(heat_loss_map, start_pos, target_pos, movement_interval=(4, 10))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
