import math
from typing import Any, List, Tuple, Optional

import numpy as np


def process_file(filename: str) -> list[Any]:
	with open(filename) as f:
		return [tuple(map(int, line.strip().split(','))) for line in f]


def dist(p1, p2):
	return (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2


def dist_euclid(p1: Tuple[int, int, int], p2: Tuple[int, int, int], squared: bool = False) -> float:
	"""Distance entre p1 et p2. Si squared=True, retourne la distance au carré."""
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	dz = p2[2] - p1[2]
	d2 = dx * dx + dy * dy + dz * dz
	return d2 if squared else math.sqrt(d2)


def sorted_distance_pairs(boxes: List[Tuple[int, int, int]], squared: bool = False) -> List[Tuple[int, int, float]]:
	"""
	Retourne la liste triée des paires (i, j, distance) pour i < j, triée par distance croissante.
	"""
	n = len(boxes)
	pairs: List[Tuple[int, int, float]] = []
	for i in range(n):
		for j in range(i + 1, n):
			d = dist_euclid(boxes[i], boxes[j], squared=squared)
			pairs.append((i, j, d))
	pairs.sort(key=lambda x: x[2])
	return pairs


def get_circuit(circuits: List[List[int]], box: int) -> Optional[List[int]]:
	"""Renvoie le circuit (liste d'indices) contenant l'indice `box`, ou None si aucun."""
	for c in circuits:
		if box in c:
			return c
	return None


"""
	si box1 appartient à un circuit, et si box2 appartient à un autre circuit, fusionner les 2 circuits en un seul
	si box 1 et box2 n'appartiennent à aucun circuit, créé un nouveau circuit constituté des 2 éléments
	si box1 est dans un circuit mais pas box2, ajouter box2 au circuit contenant box1
	si box2 est dans un circuit mais pas box1, ajouter box1 au circuit contenant box2
	si box1 et box2 sont déjà dans le même circuit, ne rien faire
"""


def part_1(boxes: List[Tuple[int, int, int]]) -> int:
	# initialiser chaque boîte comme son propre circuit (singleton)
	n = len(boxes)
	circuits: List[List[int]] = [[i] for i in range(n)]
	pairs = sorted_distance_pairs(boxes, squared=True)[:1000]
	while pairs:
		box1, box2, d = pairs.pop(0)
		circuit1 = get_circuit(circuits, box1)
		circuit2 = get_circuit(circuits, box2)
		if circuit1 and circuit2:
			if circuit1 == circuit2:
				continue
			else:
				# 2 circuits différents -> fusion
				circuit1 += circuit2
				circuits.remove(circuit2)
		else:
			if circuit1:
				circuit1.append(box2)
			elif circuit2:
				circuit2.append(box1)
			else:
				circuits.append([box1, box2])

	circuits = sorted(circuits, key=len, reverse=True)
	return np.array([len(circuits[i]) for i in range(3)], dtype=int).prod()


def part_2(boxes: List[Tuple[int, int, int]]) -> int:
	# initialiser chaque boîte comme son propre circuit (singleton)
	n = len(boxes)
	circuits: List[List[int]] = [[i] for i in range(n)]
	pairs = sorted_distance_pairs(boxes, squared=True)
	i = 0
	while pairs:
		i += 1
		box1, box2, d = pairs.pop(0)
		circuit1 = get_circuit(circuits, box1)
		circuit2 = get_circuit(circuits, box2)
		if circuit1 and circuit2:
			if circuit1 == circuit2:
				continue
			else:
				# 2 circuits différents -> fusion
				circuit1 += circuit2
				circuits.remove(circuit2)
		else:
			if circuit1:
				circuit1.append(box2)
			elif circuit2:
				circuit2.append(box1)
			else:
				circuits.append([box1, box2])
		# Si toutes les boîtes sont maintenant dans un seul circuit, retourner le dernier couple connecté
		if len(circuits) == 1:
			a, b = boxes[box1], boxes[box2]
			return a[0] * b[0]


def main() -> None:
	boxes = process_file('input.txt')
	print(f"result aoc day 8 - p1: {part_1(boxes=boxes)}")
	print(f"result aoc day 8 - p2: {part_2(boxes=boxes)}")


if __name__ == "__main__":
	main()
