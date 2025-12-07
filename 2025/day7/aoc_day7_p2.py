from typing import List


def process_file(filename: str) -> List[List[str]]:
	with open(filename) as f:
		return [list(line.rstrip("\n")) for line in f]


def count_timelines(grid: List[List[str]]) -> int:
	"""Compte le nombre de timelines atteignant le bas en utilisant une DP par ligne.

	Le rayon démarre en (start_x, 0) où 'S' est dans la première ligne.
	Si une case contient '^', toutes les timelines présentes se partagent vers (x-1,y+1) et (x+1,y+1).
	Sinon les timelines continuent vers (x,y+1).
	Les timelines qui atteignent la dernière ligne (et continuent vers y+1 hors grille) sont comptées dans le résultat.
	Complexité: O(width * height) en temps et O(width) en mémoire.

	N.B.: Remplacé l'exploration par file/DFS/BFS des timelines (exponentielle en présence de splits) par un comptage par colonne pour chaque ligne.
		Chaque cellule propage son nombre de timelines vers la ligne suivante selon la règle: obstacle '^' -> split vers x-1 et x+1 ; sinon -> x.
	"""
	width, height = len(grid[0]), len(grid)
	# trouver la position de départ 'S' sur la première ligne
	start_x = grid[0].index('S')

	# counts[x] = nombre de timelines arrivant à la colonne x à la ligne courante y
	counts = [0] * width
	counts[start_x] = 1
	result = 0

	# itérer sur chaque ligne y
	for y in range(0, height):
		row = grid[y]
		# nouvelle distribution pour la ligne y+1
		new_counts = [0] * width
		# itérer sur les colonnes
		for x, c in enumerate(counts):
			if c == 0:
				continue
			cell = row[x]
			# obstacle: split à gauche et droite
			if cell == '^':
				nx = x - 1
				if 0 <= nx < width and y + 1 < height:
					new_counts[nx] += c
				nx = x + 1
				if 0 <= nx < width and y + 1 < height:
					new_counts[nx] += c
			else:
				# propagation droite vers le bas
				if y + 1 < height:
					new_counts[x] += c
				else:
					# atteint la fin de la grille -> compter comme une timeline terminée
					result += c
		# passer à la ligne suivante
		counts = new_counts

	return result

def count_timelines_short(grid: List[List[str]]) -> int:
	width, height = len(grid[0]), len(grid)
	start_x = grid[0].index('S')
	counts = [0] * width
	counts[start_x] = 1
	result = 0
	# counts: liste length=width, counts[start_x]=1
	for y in range(height):
		new_counts = [0]*width
		for x, c in enumerate(counts):
			if c == 0: continue
			if grid[y][x] == '^':
				if 0 <= x-1 < width: new_counts[x-1] += c
				if 0 <= x+1 < width: new_counts[x+1] += c
			else:
				if y+1 < height: new_counts[x] += c
				else: result += c   # atteint la sortie
		counts = new_counts
	return result

def part_1(grid: List[List[str]]) -> int:
	# même comportement que part_2 pour l'instant
	return count_timelines(grid=grid)


def part_2(grid: List[List[str]]) -> int:
	return count_timelines_short(grid=grid)


def main() -> None:
	grid = process_file('input.txt')
	# print(f"result aoc day 7 - p1: {part_1(grid=grid)}")
	print(f"result aoc day 7 - p2: {part_2(grid=grid)}")


if __name__ == "__main__":
	main()
