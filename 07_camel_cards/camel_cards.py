import time
from collections import Counter

begin = time.time()

###

PICTURE_CARD_VALUE = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}

def hand_ordering_key(hand: list) -> list:
	hand_type, hand, _ = hand
	card_values = [int(PICTURE_CARD_VALUE.get(card, card)) for card in hand]
	return [int(hand_type[0])] + card_values

def get_type(hand: list, part2: bool) -> str:
	hand, _ = hand
	c = Counter(hand)

	if part2:
		del c["J"]
		if not c:
			return "6-Five of a kind"
		most_common_card = c.most_common()[0][0]
		hand = hand.replace("J", most_common_card)
		c = Counter(hand)

	most_common_card_count = c.most_common()[0][1]
	match most_common_card_count, len(c):
		case 5, 1: return "6-Five of a kind"
		case 4, 2: return "5-Four of a kind"
		case 3, 2: return "4-Full house"
		case 3, 3: return "3-Three of a kind"
		case 2, 3: return "2-Two pair"
		case 2, 4: return "1-One pair"
		case 1, 5: return "0-High card"
		case _, _: raise ValueError(hand, most_common_card_count, c)

def calculate_winnings(raw_hands: list, part2: bool) -> list:
	typed_hands = [[get_type(hand, part2)] + hand for hand in raw_hands]
	sorted_hands = sorted(typed_hands, key=hand_ordering_key)
	return [int(hand[-1]) * (idx+1) for idx, hand in enumerate(sorted_hands)]


hands = []
with open("input.txt") as file:
	hands = [line.strip().split() for line in file.readlines()]

p1_winnings = calculate_winnings(hands, False)
PICTURE_CARD_VALUE["J"] = 1
p2_winnings = calculate_winnings(hands, True)

print(f"Part 1: {sum(p1_winnings)}")
print(f"Part 2: {sum(p2_winnings)}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
