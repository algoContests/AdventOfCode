from typing import Any


def process_file(filename: str) -> list[Any]:
	with open(filename) as f:
		return [(line[0], int(line[1:])) for line in f]


def part_1(dial_start: int, moves: list[Any]) -> int:
	p: int = dial_start
	_dirs = {'L': -1, 'R': 1}
	pwd: int = 0
	for _direction, _distance in moves:
		p = (p + _dirs[_direction] * _distance) % 100
		pwd += 1 if p == 0 else 0
	return pwd


def part_2(dial_start: int, moves: list[Any]) -> int:
	p: int = dial_start
	_dirs = {'L': -1, 'R': 1}
	pwd: int = 0
	for _direction, _distance in moves:
		for d in range(_distance):
			p = (p + _dirs[_direction]) % 100
			pwd += 1 if p == 0 else 0
	return pwd


def main() -> None:
	l = process_file('input.txt')
	print(f"result aoc day 1 - p1: {part_1(dial_start=50, moves=l)}")
	print(f"result aoc day 1 - p2: {part_2(dial_start=50, moves=l)}")


if __name__ == "__main__":
	main()
