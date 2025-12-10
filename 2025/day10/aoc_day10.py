import re
from typing import List, Tuple, Union
from collections import deque
from pathlib import Path
import concurrent.futures
import os


def process_file(filename: Union[str, Path]) -> Tuple[List[List[bool]], List[List[List[int]]], List[List[int]]]:
	"""
	Parse `filename` lines of format:
	[pattern] (a,b,...) (c,...) {v0,v1,...}
	Returns (lights, buttons, targets)
	- lights: list of boolean lists ('.'->False, '#'=>True)
	- buttons: per-line list of actions (each action is list of indices)
	- targets: per-line list of integer target voltages (one per column)
	"""
	lights: List[List[bool]] = []
	buttons: List[List[List[int]]] = []
	targets: List[List[int]] = []

	with open(filename) as f:
		for line in f:
			line = line.strip()
			if not line:
				continue

			# extrait le motif entre crochets
			m = re.search(r'\[([^]]+)]', line)
			if not m:
				raise ValueError(f"Ligne sans motif entre crochets: {line}")
			pattern = m.group(1)
			row = [ch == '#' for ch in pattern]
			lights.append(row)
			width = len(row)

			# extrait toutes les parenthèses (actions)
			paren_groups = re.findall(r'\(([^)]*)\)', line)
			actions: List[List[int]] = []
			for grp in paren_groups:
				content = grp.strip()
				if content == "":
					actions.append([])
				else:
					indices = [int(x.strip()) for x in content.split(',') if x.strip() != ""]
					actions.append(indices)
			buttons.append(actions)

			# extrait les tensions entre accolades
			m2 = re.search(r'\{([^}]*)}', line)
			if not m2:
				raise ValueError(f"Ligne sans tensions entre accolades: {line}")
			vals = [int(x.strip()) for x in m2.group(1).split(',') if x.strip() != ""]
			if len(vals) != width:
				raise ValueError(f"Nombre de tensions ({len(vals)}) != largeur ({width}) dans la ligne: {line}")
			targets.append(vals)

	return lights, buttons, targets


def part_1(lights: List[List[bool]], buttons: List[List[List[int]]]) -> int:
	"""
	Voir implémentation précédente : BFS sur espace d'états (bitmask) pour chaque ligne.
	"""
	total_presses = 0

	for row_idx, row_pattern in enumerate(lights):
		width = len(row_pattern)
		target = 0
		for i, val in enumerate(row_pattern):
			if val:
				target |= (1 << i)

		raw_actions = buttons[row_idx] if row_idx < len(buttons) else []
		action_masks: List[int] = []
		for act in raw_actions:
			mask = 0
			for pos in act:
				if 0 <= pos < width:
					mask |= (1 << pos)
				else:
					pass
			if mask != 0:
				action_masks.append(mask)

		if target == 0:
			continue

		max_states = 1 << width
		if max_states > 1 << 22:
			raise ValueError(f"Trop grand pour un BFS direct sur la ligne {row_idx} (largeur={width})")

		visited = [-1] * max_states
		dq = deque()
		visited[0] = 0
		dq.append(0)
		found = -1

		while dq:
			s = dq.popleft()
			for a in action_masks:
				ns = s ^ a
				if visited[ns] == -1:
					visited[ns] = visited[s] + 1
					if ns == target:
						found = visited[ns]
						break
					dq.append(ns)
			if found != -1:
				break

		if found == -1:
			raise ValueError(f"Impossible d'atteindre la configuration sur la ligne {row_idx}")

		total_presses += found

	return total_presses


def solve_line_exact(args: Tuple[int, List[List[int]], List[int]]) -> Tuple[int, int]:
	"""Solve one line using OR-Tools CP-SAT.
	args = (row_idx, actions_raw, target) -> returns (row_idx, found_p)
	This formulation creates integer vars x_k >= 0 and constraints sum_k x_k * A_k[j] == target[j].
	We minimize sum_k x_k. Use a time limit (seconds) and single search worker to allow multiple processes.
	"""
	try:
		from ortools.sat.python import cp_model
	except Exception as e:
		raise RuntimeError("OR-Tools (ortools) is required. Please install with: pip install ortools") from e

	row_idx, raw_actions, target = args
	width = len(target)
	actions = [[p for p in act if 0 <= p < width] for act in raw_actions]
	actions = [a for a in actions if a]
	K = len(actions)

	# quick feasibility
	for j in range(width):
		if target[j] > 0 and not any(j in a for a in actions):
			raise ValueError(f"Impossible to cover column {j} on line {row_idx}")

	# Build matrix A_kj
	A = [[1 if j in a else 0 for j in range(width)] for a in actions]

	model = cp_model.CpModel()
	# create integer variables x_k >= 0
	x = [model.NewIntVar(0, sum(target), f'x_{k}') for k in range(K)]

	# constraints: for each column j, sum_k x_k * A[k][j] == target[j]
	for j in range(width):
		coeffs = [A[k][j] for k in range(K)]
		if any(coeffs):
			model.Add(sum(x[k] * coeffs[k] for k in range(K)) == target[j])
		else:
			# if no coeffs, target must be zero (checked earlier), but ensure
			if target[j] != 0:
				raise ValueError(f"Unsolvable column {j} on line {row_idx}")

	# objective minimize sum x_k
	obj = sum(x)
	model.Minimize(obj)

	solver = cp_model.CpSolver()
	# limit time and use single search worker so running many processes doesn't oversubscribe CPU
	solver.parameters.max_time_in_seconds = 30.0
	solver.parameters.num_search_workers = 1

	status = solver.Solve(model)
	if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
		val = int(solver.ObjectiveValue())
		return row_idx, val
	else:
		raise ValueError(f"No solution found by CP-SAT for line {row_idx} (status={status})")


def part_2(lights: List[List[bool]], buttons: List[List[List[int]]], targets: List[List[int]]) -> int:
	"""
	Exact solver for part 2: for each line, find minimal total presses x_k >= 0 integers such that
	for each column j: sum_k x_k * A_k[j] == target[j], minimizing sum_k x_k.
	This implementation is exact but potentially costly: it iterates total presses p from a lower bound
	to an upper bound (greedy) and tries to assign counts to actions via backtracking with pruning.
	"""
	tasks = []
	for row_idx, row in enumerate(lights):
		width = len(row)
		target = targets[row_idx]
		# trivial
		if all(v == 0 for v in target):
			print(f"line {row_idx}: trivial (0)")
			continue
		raw_actions = buttons[row_idx] if row_idx < len(buttons) else []
		tasks.append((row_idx, raw_actions, target))

	# run in parallel
	total_presses = 0
	with concurrent.futures.ProcessPoolExecutor(max_workers=min(os.cpu_count() or 1, len(tasks))) as ex:
		futures = {ex.submit(solve_line_exact, t): t[0] for t in tasks}
		for fut in concurrent.futures.as_completed(futures):
			row_idx = futures[fut]
			try:
				ridx, found_p = fut.result()
				print(f"line {ridx}: found={found_p}")
				total_presses += found_p
			except Exception as e:
				# surface worker exceptions
				raise

	return total_presses


def main() -> None:
	base = Path(__file__).parent
	lights, buttons, targets = process_file(base / 'input.txt')
	print(f"result aoc day 10 - p1: {part_1(lights, buttons)}")
	print(f"result aoc day 10 - p2: {part_2(lights, buttons, targets)}")


if __name__ == "__main__":
	main()
