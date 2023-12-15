import time
from collections import defaultdict, OrderedDict

begin = time.time()

###

def hash_algorithm(string: str) -> int:
	current_value = 0
	for char in string:
		current_value += ord(char)
		current_value *= 17
		current_value %= 256
	return current_value

def create_hashmap(sequence: list) -> dict:
	result = defaultdict(OrderedDict)
	for step in sequence:
		if step[-1].isdigit():
			assert step[-2] == "="
			label, focal_length = step[:-2], int(step[-1])
			result[hash_algorithm(label)][label] = focal_length
		else:
			assert step[-1] == "-"
			label = step[:-1]
			result[hash_algorithm(label)].pop(label, None)
	return result

def focusing_power(boxes: dict) -> int:
	result = 0
	for idx, box in boxes.items():
		for slot, (_, focal_length) in enumerate(box.items()):
			result += (idx + 1) * (slot + 1) * focal_length
	return result


with open("input.txt") as file:
	init_seq = file.read().strip().split(",")

hashmap = create_hashmap(init_seq)

print(f"Part 1: {sum(hash_algorithm(step) for step in init_seq)}")
print(f"Part 2: {focusing_power(hashmap)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
