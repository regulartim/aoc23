import re
import time
from math import prod

begin = time.time()

###

INVERSE_OPERATORS = {">": ("<", 1), "<": (">", -1)}

def parse_workflows(lines: list) -> dict:
	result = {}
	for line in lines:
		name, rules = line.strip().split("{")
		result[name] = []
		for rule in rules[:-1].split(","):
			if not ":" in rule:
				result[name].append(("i", None, 0, rule))
				continue
			rest, target = rule.split(":")
			cat, op, value = rest[0], rest[1], int(rest[2:])
			result[name].append((cat, op, value, target))
	return result

def decision_tree_paths(previous_path: tuple, workflows: dict, wf_name="in", idx=0) -> list:
	if wf_name == "A":
		return [previous_path]
	if wf_name == "R":
		return []
	cat, op, value, target = workflows[wf_name][idx]
	if cat == "i":
		return decision_tree_paths(previous_path, workflows, target)
	inv_op, delta = INVERSE_OPERATORS[op]
	left_path  = (*previous_path, (cat, op, value))
	right_path = (*previous_path, (cat, inv_op, value + delta))
	left_continued_paths  = decision_tree_paths(left_path, workflows, target)
	right_continued_paths = decision_tree_paths(right_path, workflows, wf_name, idx+1)
	return left_continued_paths + right_continued_paths

def accepted_ranges(path: tuple) -> dict:
	ranges = {char: (1,4001) for char in "xmas"}
	for cat, op, value in path:
		lower, upper = ranges[cat]
		ranges[cat] = (lower, min(upper, value)) if op == "<" else (max(lower, value+1), upper)
	return ranges

def check_part(part: dict, ranges: list):
	for r in ranges:
		if all(r[cat][0] <= rating < r[cat][1] for cat, rating in part.items()):
			return True
	return False


with open("input.txt") as file:
	blocks = file.read().strip().split("\n\n")
	workflow_series = parse_workflows(blocks[0].splitlines())
	part_ratings = [{k: int(v) for k, v in zip("xmas", re.findall(r"\d+", line))}
								for line in blocks[1].splitlines()]

paths = decision_tree_paths((), workflow_series)
accepted_ratings_per_path = [accepted_ranges(path) for path in paths]
accepted_p1_parts = [part for part in part_ratings if check_part(part, accepted_ratings_per_path)]
sum_of_p1_ratings = sum(sum(p.values()) for p in accepted_p1_parts)
rating_combinations = sum(prod(r[1] - r[0] for r in ranges.values())
											for ranges in accepted_ratings_per_path)

print(f"Part 1: {sum_of_p1_ratings}")
print(f"Part 2: {rating_combinations}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
