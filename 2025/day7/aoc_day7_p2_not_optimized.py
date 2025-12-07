from collections import deque
from typing import List, Optional, Any, Tuple


def process_file(filename: str) -> Any:
	with open(filename) as f:
		return [list(line.rstrip("\n")) for line in f]


def count_timelines(grid: List[List[str]]) -> int:
	width, height = len(grid[0]), len(grid)
	start_x = grid[0].index('S')
	in_grid = lambda x, y: 0 <= x < width and y < height

	q = deque([(start_x, 0)])

	splits = 0

	while q:
		x, y = q.popleft()
		if not in_grid(x, y):
			continue

		cell = grid[y][x]

		# If obstacle, split left and right (do not continue straight down)
		if cell == '^':
			# Count this split only once: replace '^' so future visits won't recount
			for dx in (-1, 1):
				nx, ny = x + dx, y + 1
				if in_grid(nx, ny):
					q.append((nx, ny))
			continue

		# Si déjà visité ou case marquée, on ignore (préservé par visited)
		# Propagation normale vers le bas
		if y + 1 < height:
			q.append((x, y + 1))
		else:
			splits += 1

	return splits


def part_1(grid) -> int:
	return


def part_2(grid) -> int:
	return count_timelines(grid=grid)


def main() -> None:
	grid = process_file('input.txt')
	# print(f"result aoc day 7 - p1: {part_1(grid=grid)}")
	print(f"result aoc day 7 - p2: {part_2(grid=grid)}")


if __name__ == "__main__":
	main()
