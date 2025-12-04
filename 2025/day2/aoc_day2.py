import math
from typing import Any, List


def process_file(filename: str) -> list[Any]:
	with open(filename) as f:
		return [tuple(map(int, line.split('-'))) for line in f.readline().split(',')]


def part_1(ranges: list[Any]) -> int:
	sum_invalids = 0
	for start, end in ranges:
		for num in range(start, end + 1):
			num_str = str(num)
			if num_str[:len(num_str) // 2] == num_str[len(num_str) // 2:]:
				sum_invalids += num
	return sum_invalids


def divisors(n: int) -> List[int]:
	"""
	Retourne la liste triée des diviseurs entiers positifs de n.
	Lève ValueError si n <= 0.
	"""
	if n <= 0:
		raise ValueError("n doit être un entier strictement positif")
	res: List[int] = []
	limit = math.isqrt(n)
	for i in range(1, limit + 1):
		if n % i == 0:
			res.append(i)
			j = n // i
			if j != i:
				res.append(j)
	return sorted(res)


def part_2(ranges: list[Any]) -> int:
	sum_invalids = 0
	# invalids = []
	for start, end in ranges:
		for num in range(start, end + 1):
			num_str = str(num)
			found: bool = False
			for div in divisors(len(num_str)):
				if found:
					break
				group_count = len(num_str) // div
				groups = [num_str[i * div: (i + 1) * div] for i in range(group_count)]
				if len(groups) > 1 and len(set(groups)) == 1:
					sum_invalids += num
					# invalids.append(num)
					found = True
	return sum_invalids


def main() -> None:
	l = process_file('input.txt')
	print(f"result aoc day 2 - p1: {part_1(ranges=l)}")
	print(f"result aoc day 2 - p2: {part_2(ranges=l)}")


if __name__ == "__main__":
	main()
