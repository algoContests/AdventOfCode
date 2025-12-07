import math
from collections import deque
from typing import Any, List


def process_file(filename: str) -> list[Any]:
	with open(filename) as f:
		# return [list(map(int, list(line.strip()))) for line in f]
		return [list(line.strip()) for line in f]


def part_1(banks: list[Any]) -> int:
	result: int = 0
	for bank in banks:
		max_power: int = 0
		for i, a in enumerate(bank):
			for j, b in enumerate(bank[i + 1:], start=i + 1):
				max_power = max(max_power, int(str(a + b)))
		result += max_power
	return result


def max_subsequence_of_length_k(bank: list[Any], k: int = 12) -> int:
	queue = deque()
	for i, digit in enumerate(bank):
		while queue and len(queue) + (len(bank) - i) > k and queue[-1] < digit:
			queue.pop()
		if len(queue) < k:
			queue.append(digit)
	return int(''.join(queue))


def part_2(banks: list[Any]) -> int:
	return sum([max_subsequence_of_length_k(b) for b in banks])


def main() -> None:
	l = process_file('input.txt')
	print(f"result aoc day 3 - p1: {part_1(banks=l)}")
	print(f"result aoc day 3 - p2: {part_2(banks=l)}")


if __name__ == "__main__":
	main()
