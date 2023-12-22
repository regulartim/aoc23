import re
import time

begin = time.time()

###

def add_tuples(s: tuple, t: tuple) -> tuple:
	return tuple(n + m for n, m in zip(s, t))

class Brick:
	def __init__(self, start: tuple, stop: tuple):
		points = []
		for idx, (a, b) in enumerate(zip(start, stop)):
			if a == b:
				continue
			for coord in range(a, b):
				new_p = list(start)
				new_p[idx] = coord
				points.append(tuple(new_p))
		self.position = tuple(points + [stop])
		self.supports = []
		self.supported_by = []
		self.disintegrated = False

	def __eq__(self, other) -> bool:
		return self.position == other.position

	def __lt__(self, other) -> bool:
		return self.position[0][-1] < other.position[0][-1]

	def __hash__(self):
		return hash(self.position)

	def __repr__(self) -> str:
		return f"{self.position[0]}~{self.position[-1]}"

	def drop(self, occupied: set) -> None:
		if self.position[0][-1] == 1:
			return
		occupied.difference_update(self.position)
		while not any(p in occupied for p in self.position) and self.position[0][-1] > 0:
			self.position = tuple(add_tuples(p, (0,0,-1)) for p in self.position)
		self.position = tuple(add_tuples(p, (0,0,1)) for p in self.position)
		occupied.update(self.position)

	def calculate_supports(self, own_idx: int, others: list):
		above = set(add_tuples(p,(0,0,1)) for p in self.position)
		for other in others[own_idx+1:]:
			if above.intersection(other.position):
				self.supports.append(other)
				other.supported_by.append(self)

	def count_collapses(self, first: bool) -> int:
		self.disintegrated = all(other.disintegrated for other in self.supported_by)
		if first:
			self.disintegrated = True
		if not self.disintegrated:
			return 0
		result = 1 + sum(other.count_collapses(False) for other in self.supports)
		return result

	def reset(self):
		self.disintegrated = False
		for other in self.supports:
			other.reset()


sand_bricks = []
with open("input.txt") as file:
	for line in file.readlines():
		numbers = [int(n) for n in re.findall(r"\d+", line)]
		sand_bricks.append(Brick(tuple(numbers[:3]), tuple(numbers[3:])))

sand_bricks.sort()

occupied_points = {p for brick in sand_bricks for p in brick.position}
for brick in sand_bricks:
	brick.drop(occupied_points)

for i, brick in enumerate(sand_bricks):
	brick.calculate_supports(i, sand_bricks)

collapse_counts = 0
unsafe_to_disintegrate = set(b.supported_by[0] for b in sand_bricks if len(b.supported_by) == 1)
for brick in unsafe_to_disintegrate:
	collapse_counts += brick.count_collapses(True) - 1
	brick.reset()

print(f"Part 1: {len(sand_bricks) - len(unsafe_to_disintegrate)}")
print(f"Part 2: {collapse_counts}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
