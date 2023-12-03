import time
from itertools import product
from math import prod

begin = time.time()

###

NEIGHBOURHOOD = list(product([-1,0,1], repeat=2))

def add_tuples(a ,b) -> tuple:
	return tuple(map(sum, zip(a, b)))

def get_neighbours(number: str, coord: tuple) -> set:
	x, y = coord
	result = []
	for i in range(len(number)):
		result += [add_tuples((x+i, y), n) for n in NEIGHBOURHOOD]
	return set(result)

def parse_numbers(lines: list) -> dict:
	result = {}
	for y, line in enumerate(lines):
		buffer = ""
		for x, char in enumerate(line.strip() + "."):
			if char.isdigit():
				buffer += char
				continue
			if buffer:
				coord = x - len(buffer), y
				result[coord] = buffer
				buffer = ""
	return result

def parse_symbols(lines: list) -> dict:
	result = {}
	for y, line in enumerate(lines):
		for x, char in enumerate(line.strip()):
			if char == "." or char.isdigit():
				continue
			result[(x,y)] = char
	return result


with open("input.txt") as file:
	inp = file.readlines()

numbers = parse_numbers(inp)
symbols = parse_symbols(inp)
gear_symbols = {k: [] for k, v in symbols.items() if v == "*"}

part_numbers = []
for coordinates, n in numbers.items():
	neighbour_coords = get_neighbours(n, coordinates)
	if symbols.keys() & neighbour_coords:
		part_numbers.append(int(n))
	for gear_coords in gear_symbols.keys() & neighbour_coords:
		gear_symbols[gear_coords].append(int(n))

gear_ratios = [prod(numbers) for numbers in gear_symbols.values() if len(numbers) == 2]

print(f"Part 1: {sum(n for n in part_numbers)}")
print(f"Part 2: {sum(gear_ratios)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
