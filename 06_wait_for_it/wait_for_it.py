import re
import time
from math import prod

begin = time.time()

###

def ways_to_win(t: int, d: int) -> int:
	counter = 0
	for hold_time in range(t+1):
		travel_dist = hold_time * (t - hold_time)
		counter += travel_dist > d
	return counter


with open("input.txt") as file:
	lines = file.readlines()

p1_times = [int(n) for n in re.findall(r"\d+", lines[0])]
p1_dists = [int(n) for n in re.findall(r"\d+", lines[1])]
p2_time = int("".join(n for n in re.findall(r"\d+", lines[0])))
p2_dist = int("".join(n for n in re.findall(r"\d+", lines[1])))

total_ways_to_win = [ways_to_win(*tup) for tup in zip(p1_times, p1_dists)]

print(f"Part 1: {prod(total_ways_to_win)}")
print(f"Part 2: {ways_to_win(p2_time, p2_dist)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
