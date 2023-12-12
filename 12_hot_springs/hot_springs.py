import time
from functools import cache

begin = time.time()

###

def unfold(springs: str, groups: tuple, factor: int) -> tuple:
	springs = "?".join(springs for _ in range(factor))
	groups = groups*factor
	return (springs, groups)

@cache
def count_arrangemens(springs: str, groups: tuple, matched_group_count: int, current_seq_len: int) -> int:
	group_len = groups[matched_group_count] if matched_group_count < len(groups) else 0

	if not springs:
		matched_group_count += 1 if current_seq_len > 0 else 0
		if current_seq_len != group_len:
			return 0
		if matched_group_count != len(groups):
			return 0
		return 1

	fwd_state = (matched_group_count, current_seq_len)
	add_to_seq_state = (matched_group_count, current_seq_len+1)
	add_group_state = (matched_group_count+1, 0)
	match springs[0], current_seq_len > 0, current_seq_len == group_len:
		case ".", True,  True : new_states = [add_group_state]
		case ".", False, _    : new_states = [fwd_state]
		case "#", _,     False: new_states = [add_to_seq_state]
		case "?", True,  True : new_states = [add_group_state]
		case "?", True,  False: new_states = [add_to_seq_state]
		case "?", False, _    : new_states = [add_to_seq_state, fwd_state]
		case _,   _,     _    : new_states = []
	return sum(count_arrangemens(springs[1:], groups, *new) for new in new_states)


condition_records = []
with open("input.txt") as file:
	for line in file.readlines():
		spr, nums = line.strip().split()
		nums = tuple(int(n) for n in nums.split(","))
		condition_records.append((spr, nums))

starting_state = (0,0)
unfolded_records = (unfold(*row, 5) for row in condition_records)
p1_counts = (count_arrangemens(*row, *starting_state) for row in condition_records)
p2_counts = (count_arrangemens(*row, *starting_state) for row in unfolded_records)

print(f"Part 1: {sum(p1_counts)}")
print(f"Part 2: {sum(p2_counts)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
