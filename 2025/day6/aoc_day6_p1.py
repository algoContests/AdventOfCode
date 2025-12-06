from typing import List, Optional, Any
import numpy as np


def process_file(filename: str) -> tuple[Any, Any]:
	with open(filename) as f:
		data = [line.strip() for line in f]
		numbers = np.loadtxt(data[:-1], dtype=int).T
		operators = data[-1].split()
	return numbers, operators


def part_1(numbers, operators) -> int:
	return sum(numbers[i].sum() if op == '+' else numbers[i].prod() for i, op in enumerate(operators))


def main() -> None:
	numbers, operators = process_file('input.txt')
	print(f"result aoc day 6 - p1: {part_1(numbers, operators)}")


if __name__ == "__main__":
	main()
