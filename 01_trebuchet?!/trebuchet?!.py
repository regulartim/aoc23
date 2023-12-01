import re
import time

begin = time.time()

###

SPELLED_DIGITS_TO_INT = { word: int(number) + 1 for number, word
	in enumerate(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]) }
DIGIT_STR_TO_INT = {str(n): n for n in range(10)}
ALL_DIGITS_TO_INT = SPELLED_DIGITS_TO_INT | DIGIT_STR_TO_INT


def get_two_digit_numbers(lines: list, pattern: str) -> list:
	extracted_digits = [re.findall(pattern, line) for line in lines]
	result = []
	for e, line in zip(extracted_digits, lines):
		first, last = e[0], e[-1]
		first_as_int, last_as_int = ALL_DIGITS_TO_INT[first], ALL_DIGITS_TO_INT[last]
		result.append(10*first_as_int + last_as_int)
	return result


with open("input.txt") as file:
	inp = file.readlines()

p1_pattern = r"\d"
p2_pattern = fr"(?=(\d|{'|'.join(SPELLED_DIGITS_TO_INT)}))"

print(f"Part 1: {sum(get_two_digit_numbers(inp, p1_pattern))}")
print(f"Part 2: {sum(get_two_digit_numbers(inp, p2_pattern))}")

###

end = time.time()
runtime_in_ms = round((end - begin)*1000, 3)
print(f"Runtime: {runtime_in_ms:.3f} ms")
