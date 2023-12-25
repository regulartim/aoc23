import re
import time
from itertools import combinations
import numpy as np
import z3

begin = time.time()

###

TEST_AREA = (200000000000000,400000000000000)

def crossing_point(a: list, b: list) -> tuple:
	ax, ay, _, avx, avy, _ = a
	bx, by, _, bvx, bvy, _ = b
	left_side = [[avx, -bvx], [avy, -bvy]]
	right_side = [bx-ax, by-ay]
	try:
		factors = np.linalg.inv(left_side).dot(right_side)
	except:
		return None
	if any (f < 0 for f in factors):
		return None
	result = [ax + factors[0] * avx, ay + factors[0] * avy ]
	return tuple(result)

def throwing_position(hails: list) -> tuple:
	x, y, z, vx, vy, vz = z3.Reals("x y z vx vy vz")
	solver = z3.Solver()
	for idx, h in enumerate(hails):
		hx, hy, hz, hvx, hvy, hvz = h
		t = z3.Real(f"t{idx}")
		solver.add(t >= 0)
		solver.add(hx + hvx * t == x + vx * t)
		solver.add(hy + hvy * t == y + vy * t)
		solver.add(hz + hvz * t == z + vz * t)
	solver.check()
	m = solver.model()
	return[m[d].as_long() for d in [x,y,z]]


with open("input.txt") as file:
	hailstones = [[int(n) for n in re.findall(r"-?\d+", line)] for line in file.readlines()]

crossings = [crossing_point(h1, h2) for h1, h2 in combinations(hailstones, 2)]
within_test_area = [c for c in crossings if c and all(TEST_AREA[0] <= d <= TEST_AREA[1] for d in c)]

print(f"Part 1: {len(within_test_area)}")
print(f"Part 2: {sum(throwing_position(hailstones))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
