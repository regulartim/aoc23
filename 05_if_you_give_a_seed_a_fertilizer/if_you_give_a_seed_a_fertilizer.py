import re
import time

begin = time.time()

###

def get_destination(source: int, m: list) -> int:
	for r_start, source_r_start, r_len in m:
		if source_r_start <= source < source_r_start + r_len:
			return r_start + source - source_r_start
	return source

def get_location(category: int, maps: list) -> int:
	for m in maps:
		category = get_destination(category, m)
	return category

def get_overlap(a: tuple, b: tuple) -> tuple:
	start, stop = max(a[0], b[0]), min(a[1], b[1])
	if start >= stop:
		return None
	return (start, stop)

def get_destination_ranges(source_ranges: list, m: list) -> list:
	result =[]
	while source_ranges:
		r = source_ranges.pop()
		for dest_start, source_start, r_len in m:
			overlap = get_overlap(r, (source_start, source_start+r_len))
			if not overlap:
				continue
			delta = dest_start - source_start
			result.append((delta + overlap[0], delta + overlap[1]))
			source_ranges += [(r[0], overlap[0]), (overlap[1], r[1])]
			break
		else:
			result.append(r)
		source_ranges = [r for r in source_ranges if r[0] < r[1]]
	return result

def get_location_ranges(ranges: list, maps: list) -> list:
	for m in maps:
		ranges = get_destination_ranges(ranges, m)
	return ranges


with open("input.txt") as file:
	blocks = file.read().split("\n\n")

seeds = [int(n) for n in re.findall(r"\d+", blocks[0])]
mappings = []
for block in blocks[1:]:
	mapping = []
	for line in block.strip().splitlines()[1:]:
		mapping.append([int(n) for n in line.split()])
	mappings.append(mapping)

locations = [get_location(seed, mappings) for seed in seeds]
seed_ranges = [(start, start+length) for start, length in zip(seeds[0::2], seeds[1::2])]
location_ranges = get_location_ranges(seed_ranges, mappings)

print(f"Part 1: {min(locations)}")
print(f"Part 2: {min(location_ranges)[0]}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
