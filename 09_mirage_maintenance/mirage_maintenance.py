import re
import time

begin = time.time()

###

def calculate_differences(sequence: list) -> list:
	result = []
	for n, m in zip(sequence, sequence[1:]):
		result.append(m-n)
	return result

def calculate_triangle(sequence: list) -> list:
	triangle = [sequence]
	while any(n != 0 for n in triangle[-1]):
		triangle.append(calculate_differences(triangle[-1]))
	return triangle

def extrapolate_history(sequence: list) -> list:
	triangle = calculate_triangle(sequence)
	delta_start, delta_end = 0, 0
	for layer in reversed(triangle):
		delta_start = layer[0] - delta_start
		delta_end += layer[-1]
	return [delta_start] + sequence + [delta_end]


with open("input.txt") as file:
	histories = [[int(n) for n in re.findall(r"-?\d+", line)] for line in file.readlines()]

extrapolated = [extrapolate_history(h) for h in histories]

print(f"Part 1: {sum(h[-1] for h in extrapolated)}")
print(f"Part 2: {sum(h[0] for h in extrapolated)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
