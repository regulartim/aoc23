import re
import time

begin = time.time()

###

def get_matches(card: list) -> set:
	winning, ours = card
	return set(winning) & set(ours)


scratchcards = []
with open("input.txt") as file:
	for line in file.readlines():
		scratchcard = [[int(n) for n in re.findall(r"\d+", part)]
							for part in line.split(":")[1].split("|")]
		scratchcards.append(scratchcard)

matches = [len(get_matches(sc)) for sc in scratchcards]

card_counts = [1 for _ in enumerate(matches)]
for idx, match_count in enumerate(matches):
	for i in range(match_count):
		other_card_idx = idx + 1 + i
		if other_card_idx < len(card_counts):
			card_counts[other_card_idx] += card_counts[idx]

print(f"Part 1: {sum(2**(m-1) if m > 0 else 0 for m in matches)}")
print(f"Part 2: {sum(card_counts)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
