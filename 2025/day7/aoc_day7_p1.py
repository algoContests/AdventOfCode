from collections import deque
from typing import List, Optional, Any, Tuple


def process_file(filename: str) -> Any:
	with open(filename) as f:
		return [list(line.rstrip("\n")) for line in f]


def count_splits(grid: List[List[str]]) -> Tuple[int, List[List[str]]]:
	width, height = len(grid[0]), len(grid)
	start_x = grid[0].index('S')
	in_grid = lambda x, y: 0 <= x < width and y < height

	q = deque([(start_x, 0)])
	visited = {(start_x, 0)}

	splits = 0

	while q:
		x, y = q.popleft()
		if not in_grid(x, y):
			continue

		cell = grid[y][x]

		# If obstacle, split left and right (do not continue straight down)
		if cell == '^':
			# Count this split only once: replace '^' so future visits won't recount
			splits += 1
			grid[y][x] = '|'  # optionnel : marquer pour affichage
			for dx in (-1, 1):
				nx, ny = x + dx, y + 1
				if in_grid(nx, ny):
					visited.add((nx, ny))
					q.append((nx, ny))
			continue

		# Si déjà visité ou case marquée, on ignore (préservé par visited)
		# Propagation normale vers le bas
		if y + 1 < height and (x, y + 1) not in visited:
			visited.add((x, y + 1))
			grid[y][x] = '|'  # optionnel : marquer le chemin
			q.append((x, y + 1))
		else:
			grid[y][x] = '|'  # optionnel : marquer la fin

	return splits, grid


def part_1(grid) -> int:
	count, new_grid = count_splits(grid=grid)
	# for line in new_grid:
	# 	print(''.join(line))
	return count


def part_2(inputs) -> int:
	return


def main() -> None:
	grid = process_file('input.txt')
	for line in grid:
		print(''.join(line))
	print(f"result aoc day 7 - p1: {part_1(grid=grid)}")
	# print(f"result aoc day 7 - p2: {part_2(inputs)}")


if __name__ == "__main__":
	main()
