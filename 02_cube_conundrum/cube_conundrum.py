import time
from collections import defaultdict
from math import prod

begin = time.time()

###

BAG_CONTENT = {"red": 12, "green": 13, "blue": 14}

def parse_subgame(subgame: str) -> dict:
	result = {}
	for s in subgame.split(","):
		n, colour = s.split()
		result[colour] = int(n)
	return result

def parse_game(line: str) -> list:
	_ , game = line.split(":")
	return [parse_subgame(g) for g in game.split(";")]

def is_possible(game: list) -> bool:
	for subgame in game:
		for colour, n in subgame.items():
			if BAG_CONTENT[colour] < n:
				return False
	return True

def get_fewest_cube_count(game: list) -> dict:
	result = defaultdict(int)
	for subgame in game:
		for colour, n in subgame.items():
			result[colour] = max(n, result[colour])
	return result


with open("input.txt") as file:
	games = [parse_game(line) for line in file]

possible_games = [is_possible(game) for game in games]
fewest_cube_counts = [get_fewest_cube_count(game) for game in games]
powers = [prod(c.values()) for c in fewest_cube_counts]

print(f"Part 1: {sum(idx+1 for idx, p in enumerate(possible_games) if p)}")
print(f"Part 2: {sum(powers)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
