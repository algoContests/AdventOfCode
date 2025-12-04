from typing import List, Tuple


def process_file(filename: str) -> List[List[str]]:
	with open(filename) as f:
		return [list(line.strip()) for line in f]


# Voisins en 8 directions, constant réutilisable
_NEIGHBORS: Tuple[Tuple[int, int], ...] = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),)


def count_adjacent_rolls_8_directions(grid: List[List[str]], row: int, col: int) -> int:
	rows = len(grid)
	cols = len(grid[0]) if rows > 0 else 0
	# Utilise une compréhension génératrice pour compter proprement
	return sum(1 for dr, dc in _NEIGHBORS if 0 <= row + dr < rows and 0 <= col + dc < cols and grid[row + dr][col + dc] == '@')


def get_removable_rolls(grid: List[List[str]]) -> List[Tuple[int, int]]:
	# Parcours la grille et collecte les positions supprimables
	return [(i, j) for i, line in enumerate(grid) for j, tile in enumerate(line) if tile == '@' and count_adjacent_rolls_8_directions(grid, i, j) < 4]


def part_1(grid: List[List[str]]) -> int:
	return len(get_removable_rolls(grid))


def part_2(grid: List[List[str]]) -> int:
	total_removed = 0  # Répéter jusqu'à ce qu'il n'y ait plus de rouleaux supprimables
	while removable := get_removable_rolls(grid):
		for i, j in removable:
			grid[i][j] = '.'
		total_removed += len(removable)
	return total_removed


def main() -> None:
	grid = process_file('input.txt')
	print(f"result aoc day 4 - p1: {part_1(grid=grid)}")
	print(f"result aoc day 4 - p2: {part_2(grid=grid)}")


if __name__ == "__main__":
	main()
