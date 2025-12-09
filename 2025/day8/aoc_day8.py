import math
from typing import List, Tuple


def process_file(filename: str) -> list[tuple[int, ...]]:
	with open(filename) as f:
		return [tuple(map(int, line.split(','))) for line in f]


def calculate_distances(boxes: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
	return sorted(((i, j, sum((boxes[j][k] - boxes[i][k]) ** 2 for k in range(3))) for i in range(len(boxes)) for j in range(i + 1, len(boxes))), key=lambda x: x[2])


def find_circuit(circuits: List[List[int]], box: int) -> List[int]:
	return next((c for c in circuits if box in c), [])


def part_1(boxes: List[Tuple[int, int, int]]) -> int:
	circuits = [[i] for i in range(len(boxes))]
	pairs = calculate_distances(boxes)[:1000]

	for box1, box2, _ in pairs:
		circuit1, circuit2 = find_circuit(circuits, box1), find_circuit(circuits, box2)
		if circuit1 != circuit2:
			circuit1.extend(circuit2)
			circuits.remove(circuit2)

	return math.prod(sorted((len(c) for c in circuits), reverse=True)[:3])


def part_2(boxes: List[Tuple[int, int, int]]) -> int:
	circuits = [[i] for i in range(len(boxes))]
	pairs = calculate_distances(boxes)

	for box1, box2, _ in pairs:
		circuit1, circuit2 = find_circuit(circuits, box1), find_circuit(circuits, box2)
		if circuit1 != circuit2:
			circuit1.extend(circuit2)
			circuits.remove(circuit2)
		if len(circuits) == 1:
			a, b = boxes[box1], boxes[box2]
			return a[0] * b[0]


def main() -> None:
	boxes = process_file('input.txt')
	print(f"result aoc day 8 - p1: {part_1(boxes)}")
	print(f"result aoc day 8 - p2: {part_2(boxes)}")


if __name__ == "__main__":
	main()
