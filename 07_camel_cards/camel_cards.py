import time
from collections import Counter

begin = time.time()

###

PICTURE_CARD_VALUE = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

def hand_type(hand: str, part2: bool) -> tuple:
	card_counts = Counter(hand)
	if part2:
		del card_counts["J"]
		most_common_card = card_counts.most_common()[0][0] if card_counts else "A"
		hand = hand.replace("J", most_common_card)
		card_counts = Counter(hand)

	most_common_card_count = card_counts.most_common()[0][1]
	match most_common_card_count, len(card_counts):
		case 5, 1: return (6, "Five of a kind")
		case 4, 2: return (5, "Four of a kind")
		case 3, 2: return (4, "Full house")
		case 3, 3: return (3, "Three of a kind")
		case 2, 3: return (2, "Two pair")
		case 2, 4: return (1, "One pair")
		case 1, 5: return (0, "High card")
		case _, _: raise ValueError(hand, most_common_card_count, card_counts)

def hand_ordering_key(play: tuple, part2: bool) -> tuple:
	hand, _ = play
	type_idx, _ = hand_type(hand, part2)
	card_values = [int(PICTURE_CARD_VALUE.get(card, card)) for card in hand]
	return (type_idx, *card_values)

def calculate_winnings(sorted_plays: list) -> list:
	winnings = []
	for idx, play in enumerate(sorted_plays):
		_, bid = play
		rank = idx + 1
		winnings.append(int(bid) * rank)
	return winnings


with open("input.txt") as file:
	plays = [tuple(line.strip().split()) for line in file.readlines()]

plays.sort(key=lambda play: hand_ordering_key(play, part2=False))
p1_winnings = calculate_winnings(plays)

PICTURE_CARD_VALUE["J"] = 1
plays.sort(key=lambda play: hand_ordering_key(play, part2=True))
p2_winnings = calculate_winnings(plays)

print(f"Part 1: {sum(p1_winnings)}")
print(f"Part 2: {sum(p2_winnings)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
