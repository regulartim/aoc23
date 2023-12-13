import time

begin = time.time()

###

def cols(rows: list) -> list:
	return ["".join(col) for col in zip(*rows)]

def str_distance(s: str, t: str) -> int:
	return sum(a != b for a, b in zip(s, t))

def reflection_lines(rows: list) -> dict:
	''' Returns mapping: numbers of smudges to index of reflection line '''
	result = {}
	for idx, (a, b) in enumerate(zip(rows, rows[1:])):
		dist = str_distance(a, b)
		if dist > 1:
			continue
		for a, b in zip(reversed(rows[:idx]), rows[idx+2:]):
			dist += str_distance(a, b)
		result[dist] = idx + 1
	return result

def solve(rows: list, part2: bool) -> int:
	horizontals = reflection_lines(rows)
	verticals = reflection_lines(cols(rows))
	smudges = 1 if part2 else 0
	return 100 * horizontals.get(smudges, 0) + verticals.get(smudges, 0)


with open("input.txt") as file:
	patterns = [[line.strip() for line in block.splitlines()] for block in file.read().split("\n\n")]

print(f"Part 1: {sum(solve(p, False) for p in patterns)}")
print(f"Part 2: {sum(solve(p, True) for p in patterns)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
