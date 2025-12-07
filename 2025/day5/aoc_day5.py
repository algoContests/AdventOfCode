from typing import List, Optional
from bisect import bisect_right, bisect_left


def process_file(filename: str) -> tuple[list[tuple[int, int]], set]:
	# Collecte des intervalles et des entiers disponibles sans matérialiser de grands sets
	intervals: list[tuple[int, int]] = []
	avail_set: set[int] = set()
	with open(filename) as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			if '-' in line:
				start, end = map(int, line.split('-'))
				intervals.append((start, end))
			else:
				avail_set.add(int(line))

	# Fusionner les intervalles chevauchants pour réduire le nombre de comparaisons
	if not intervals:
		return [], avail_set
	intervals.sort()  # triés par leur début pour faciliter la fusion
	merged: list[list[int]] = [list(intervals[0])]
	for s, e in intervals[1:]:
		if s <= merged[-1][1] + 1:
			# chevauchement ou contiguïté => étendre
			merged[-1][1] = max(merged[-1][1], e)
		else:
			merged.append([s, e])

	# Retourner des tuples immuables
	return [(s, e) for s, e in merged], avail_set


def binary_search(a, x):
	i = bisect_left(a, x)
	return i < len(a) and a[i] == x


def bisect_right_custom(a: List[int], x: int) -> int:
	"""Retourne l'indice d'insertion à droite de x dans la liste triée a."""
	lo = 0
	hi = len(a)
	while lo < hi:
		mid = (lo + hi) // 2
		if x < a[mid]:
			hi = mid
		else:
			lo = mid + 1
	return lo


def part_1(fresh_intervals: list[tuple[int, int]], avail_ing: set[int]) -> int:
	# Préparer des listes pour la recherche binaire
	starts = [s for s, _ in fresh_intervals]
	ends = [e for _, e in fresh_intervals]
	count = 0
	for x in avail_ing:
		# trouver l'intervalle dont le début est le plus grand <= x.
		# Cela permet de localiser rapidement l'intervalle potentiel contenant x
		# N.B.: bisect_left(l, x) : première position où insérer x (permet de tester l'existen
		# 		bisect_right(l, x) : dernière position où insérer x
		# i = bisect_right(starts, x) - 1
		i = bisect_right_custom(starts, x) - 1
		if i >= 0 and x <= ends[i]:
			count += 1
	return count


def part_2(fresh_intervals: list[tuple[int, int]], avail_ing: set[int]) -> int:
	return sum([(e - s + 1) for s, e in fresh_intervals])


def main() -> None:
	fresh_intervals, avail_ing = process_file('input.txt')
	print(f"result aoc day 5 - p1: {part_1(fresh_intervals, avail_ing)}")
	print(f"result aoc day 5 - p2: {part_2(fresh_intervals, avail_ing)}")


if __name__ == "__main__":
	main()
