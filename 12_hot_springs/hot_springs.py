import time
from functools import cache

begin = time.time()

###

def unfold(springs: str, groups: tuple, factor: int) -> tuple:
	springs = "?".join(springs for _ in range(factor))
	groups = groups*factor
	return (springs, groups)

def next_states(springs: str, groups: tuple, current_seq_len: int):
	forward_state       = (springs[1:], groups, current_seq_len)
	add_to_seq_state    = (springs[1:], groups, current_seq_len + 1)
	seq_completed_state = (springs[1:], groups[1:], 0)

	empty_sequence     = current_seq_len == 0
	completed_sequence = current_seq_len == groups[0]
	match springs[0], empty_sequence, completed_sequence:
		case ".", _,    True : yield seq_completed_state
		case ".", True, _    : yield forward_state
		case "#", _,    False: yield add_to_seq_state
		case "?", _,    True : yield seq_completed_state
		case "?", True, _    : yield from (add_to_seq_state, forward_state)
		case "?", _,    _    : yield add_to_seq_state
		case _,   _,    _    : pass

@cache
def count_arrangemens(springs: str, groups: tuple, current_seq_len: int) -> int:
	if not groups:
		if "#" in springs:
			return 0
		return 1

	if not springs:
		if current_seq_len == groups[0]:
			groups = groups[1:]
		if groups:
			return 0
		return 1

	return sum(count_arrangemens(*state) for state in next_states(springs, groups, current_seq_len))


condition_records = []
with open("input.txt") as file:
	for line in file.readlines():
		spr, nums = line.strip().split()
		nums = tuple(int(n) for n in nums.split(","))
		condition_records.append((spr, nums))

unfolded_records = (unfold(*row, 5) for row in condition_records)
p1_counts = (count_arrangemens(*row, 0) for row in condition_records)
p2_counts = (count_arrangemens(*row, 0) for row in unfolded_records)

print(f"Part 1: {sum(p1_counts)}")
print(f"Part 2: {sum(p2_counts)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
