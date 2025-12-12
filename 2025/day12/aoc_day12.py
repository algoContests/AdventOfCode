import sys

import re
from typing import Dict, List, Tuple
import time
import os
import concurrent.futures


def debug(*args):
	# return
	print(*args, file=sys.stderr, flush=True)


def process_file(filename: str) -> Tuple[Dict[str, List[str]], List[dict]]:
	"""Lit le fichier d'entrée et retourne :
	- shapes : dict lettre -> liste de chaînes (lignes de la forme)
	- grids  : liste de dicts avec keys 'width','height','counts'
	"""
	with open(filename) as f:
		lines = [ln.rstrip('\n') for ln in f]

	shapes: Dict[str, List[str]] = {}
	alpha = 'ABCDEF'
	i = 0
	# Parse les blocs numérotés (0:, 1:, ...)
	while i < len(lines):
		m = re.match(r'^(\d+):\s*$', lines[i])
		if m:
			idx = int(m.group(1))
			letter = alpha[idx] if idx < len(alpha) else f'SHAPE{idx}'
			i += 1
			rows: List[str] = []
			# Collecte les lignes de la forme jusqu'à une ligne vide ou un nouveau bloc
			while i < len(lines) and lines[i].strip() != '' and not re.match(r'^\d+:\s*$', lines[i]):
				rows.append(lines[i])
				i += 1
			shapes[letter] = rows
		else:
			i += 1

	# Parse les spécifications de grilles du type 'WxH: counts...'
	grids: List[dict] = []
	for line in lines:
		m = re.match(r'^(\d+)x(\d+):\s*(.+)$', line)
		if m:
			w, h = int(m.group(1)), int(m.group(2))
			counts = [int(x) for x in m.group(3).split()]
			grids.append({'width': w, 'height': h, 'counts': counts})

	return shapes, grids


# --- utilitaires pour rotation / placement ---


def rotate90(shape: List[str]) -> List[str]:
	"""Retourne la rotation de 90 degrés (horaire) de la forme."""
	h = len(shape)
	w = len(shape[0]) if h > 0 else 0
	rot = []
	for x in range(w):
		row = ''.join(shape[h - 1 - y][x] for y in range(h))
		rot.append(row)
	return rot


def all_rotations(shape: List[str]) -> List[List[str]]:
	"""Retourne les 4 rotations (0,90,180,270) en évitant les duplications."""
	rots = []
	cur = shape
	for _ in range(4):
		if cur not in rots:
			rots.append(cur)
		cur = rotate90(cur)
	return rots


def shape_offsets(shape: List[str]) -> Tuple[List[Tuple[int, int]], int]:
	"""Retourne la liste des offsets (sx,sy) des '#' et l'aire (nombre de '#')."""
	offsets = []
	for y, row in enumerate(shape):
		for x, ch in enumerate(row):
			if ch == '#':
				offsets.append((x, y))
	return offsets, len(offsets)


# backtracking solver (existential: find full placement)

def solve_grid_full(width: int, height: int, shapes: Dict[str, List[str]], counts: List[int]) -> Tuple[bool, List[List[str]]]:
	"""Optimized: try to place all instances using bitmask operations, MRV ordering and memoization.
	Returns (True, solution_grid) if a full placement exists.
	"""
	alpha = 'ABCDEF'
	n_cells = width * height
	if n_cells > 60:
		# for very large grids, still OK since Python int is arbitrary precision, but placement lists may explode
		pass

	# map cell (x,y) -> bit index
	def cell_bit(x, y):
		return 1 << (y * width + x)

	# Precompute rotations and their placement bitmasks for each shape type
	shape_types = []  # list of dicts: {'letter','placements': [bitmask], 'count','area'}
	for idx, cnt in enumerate(counts):
		letter = alpha[idx]
		shape = shapes.get(letter)
		if not shape:
			shape_types.append({'letter': letter, 'placements': [], 'count': cnt, 'area': 0})
			continue
		rots = all_rotations(shape)
		seen = set()
		placements = []
		area = 0
		for r in rots:
			key = tuple(r)
			if key in seen:
				continue
			seen.add(key)
			h = len(r)
			w = len(r[0]) if h > 0 else 0
			offsets, a = shape_offsets(r)
			if a == 0:
				continue
			area = max(area, a)
			# enumerate placements where the bounding box fits
			for y0 in range(0, height - h + 1):
				for x0 in range(0, width - w + 1):
					bm = 0
					ok = True
					for ox, oy in offsets:
						x = x0 + ox
						y = y0 + oy
						if x < 0 or y < 0 or x >= width or y >= height:
							ok = False
							break
						bm |= cell_bit(x, y)
					if ok:
						placements.append(bm)
		shape_types.append({'letter': letter, 'placements': placements, 'count': cnt, 'area': area})

	# Quick impossibility: not enough placements for required count
	for st in shape_types:
		if st['count'] > 0 and len(st['placements']) == 0:
			return False, [['.' for _ in range(width)] for _ in range(height)]

	# Order types by heuristic: fewest placements first (MRV) and larger area
	order = list(range(len(shape_types)))
	order.sort(key=lambda i: (len(shape_types[i]['placements']) if shape_types[i]['placements'] else 10 ** 9, -shape_types[i]['area']))

	# Mutable remaining counts aligned to order
	counts_ordered = [shape_types[i]['count'] for i in order]

	# Precompute total area needed
	area_needed_initial = sum(st['area'] * st['count'] for st in shape_types)

	# memoization: store seen states that failed: (occupied_bitmask, tuple(counts_ordered))
	seen_fail = set()

	solution_grid = [['.' for _ in range(width)] for _ in range(height)]

	# helper to convert occupied bitmask to grid letters later: we will also keep a placement list of (letter,bm)

	def dfs(occupied: int, counts_curr: List[int], placements_used: List[Tuple[int, int]]) -> bool:
		# check memo
		state = (occupied, tuple(counts_curr))
		if state in seen_fail:
			return False
		# area pruning: count remaining occupied cells available
		empty_cells = n_cells - occupied.bit_count()
		remaining_area = 0
		for i, cnt in enumerate(counts_curr):
			if cnt > 0:
				st = shape_types[order[i]]
				remaining_area += st['area'] * cnt
		if remaining_area > empty_cells:
			seen_fail.add(state)
			return False
		# if all zero
		if all(c == 0 for c in counts_curr):
			# build grid from placements_used
			for y in range(height):
				for x in range(width):
					solution_grid[y][x] = '.'
			for letter_idx, bm in placements_used:
				letter = shape_types[order[letter_idx]]['letter']
				# set letter on bits
				b = bm
				while b:
					bit = b & -b
					pos = (bit.bit_length() - 1)
					x = pos % width
					y = pos // width
					solution_grid[y][x] = letter
					b -= bit
			return True
		# choose next variable: MRV - index with counts>0 and fewest available placements given occupied
		best_i = -1
		best_options = None
		best_len = None
		for i, cnt in enumerate(counts_curr):
			if cnt <= 0:
				continue
			st = shape_types[order[i]]
			# compute placements not overlapping
			opts = []
			for p in st['placements']:
				if (p & occupied) == 0:
					opts.append(p)  # early exit if too many
			if best_len is None or len(opts) < best_len:
				best_len = len(opts)
				best_options = opts
				best_i = i
				if best_len == 0:
					break
		# if some type has zero options -> dead end
		if best_len == 0:
			seen_fail.add(state)
			return False
		# iterate placements for chosen type
		# try placements in arbitrary order; could add ordering
		for p in best_options:
			# place one instance
			counts_curr[best_i] -= 1
			placements_used.append((best_i, p))
			if dfs(occupied | p, counts_curr, placements_used):
				return True
			# backtrack
			placements_used.pop()
			counts_curr[best_i] += 1
		# no placement leads to solution
		seen_fail.add(state)
		return False

	ok = dfs(0, counts_ordered, [])
	if not ok:
		return False, [['.' for _ in range(width)] for _ in range(height)]
	return True, solution_grid


def process_grid_task(args):
	"""Fonction au niveau module pour exécuter solve_grid_full dans un worker.
	args = (gi, g, shapes)
	Retourne (gi, ok, sol, dur)
	"""
	gi, g, shapes = args
	start = time.time()
	ok, sol = solve_grid_full(g['width'], g['height'], shapes, g['counts'])
	dur = time.time() - start
	return gi, ok, sol, dur


# Update part_1 to use multiprocessing when requested and display timing

def part_1(shapes: Dict[str, List[str]], grids: List[dict], workers: int = 1) -> int:
	"""Pour chaque grille demandée, tente de placer toutes les instances; si possible, incrémente le compteur de grilles résolues.
	Si workers > 1, traite les grilles en parallèle avec ProcessPoolExecutor (fallback ThreadPoolExecutor si nécessaire).
	Retourne le nombre de grilles pour lesquelles la solution complète a été trouvée.
	Affiche le temps d'exécution global et par grille.
	"""
	start_all = time.time()
	success_count = 0
	results = [None] * len(grids)
	if workers is None or workers < 1:
		workers = 1
	# Sequential path
	if workers == 1:
		for gi, g in enumerate(grids):
			start = time.time()
			debug(f"\nTrying to fully fill grid #{gi} {g['width']}x{g['height']} counts={g['counts']}")
			ok, sol = solve_grid_full(g['width'], g['height'], shapes, g['counts'])
			dur = time.time() - start
			if ok:
				success_count += 1
				debug(f"Grid #{gi} fully filled (time {dur:.3f}s)")
				for row in sol:
					debug(''.join(row))
			else:
				debug(f"Grid #{gi} cannot be fully filled (time {dur:.3f}s)")
			results[gi] = (ok, sol, dur)
	else:
		# Parallel path using processes with fallback
		max_workers = min(workers, os.cpu_count() or 1)
		args = [(gi, g, shapes) for gi, g in enumerate(grids)]
		grid_map = {gi: g for gi, g in enumerate(grids)}
		use_thread = False
		try_process = True
		# decide whether process pool is safe: if main module has no __file__ (launched from stdin), ProcessPool may fail
		main_has_file = hasattr(sys.modules.get('__main__', None), '__file__')
		if not main_has_file:
			debug('Main process has no __file__; forcing ThreadPoolExecutor (spawn would fail)')
			use_thread = True
		else:
			use_thread = False
		# try process pool if allowed
		if not use_thread:
			try:
				with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as exc:
					futures = {exc.submit(process_grid_task, a): a[0] for a in args}
					for fut in concurrent.futures.as_completed(futures):
						orig_gi = futures[fut]
						try:
							res_gi, ok, sol, dur = fut.result()
						except Exception as e:
							res_gi = orig_gi
							ok = False
							sol = [['.' for _ in range(grid_map[res_gi]['width'])] for _ in range(grid_map[res_gi]['height'])]
							dur = None
							debug(f"Worker for grid #{res_gi} raised: {e}")
						if ok:
							success_count += 1
							debug(f"Grid #{res_gi} fully filled (worker) (time {dur:.3f}s)")
							for row in sol:
								debug(''.join(row))
						else:
							debug(f"Grid #{res_gi} cannot be fully filled (worker)")
						results[res_gi] = (ok, sol, dur)
			except (RuntimeError, concurrent.futures.process.BrokenProcessPool, FileNotFoundError) as e:
				debug(f"Process pool failed with: {e}; falling back to ThreadPoolExecutor")
				use_thread = True
		# threads fallback
		if use_thread:
			with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exc:
				futures = {exc.submit(process_grid_task, a): a[0] for a in args}
				for fut in concurrent.futures.as_completed(futures):
					orig_gi = futures[fut]
					try:
						res_gi, ok, sol, dur = fut.result()
					except Exception as e:
						res_gi = orig_gi
						ok = False
						sol = [['.' for _ in range(grid_map[res_gi]['width'])] for _ in range(grid_map[res_gi]['height'])]
						dur = None
						debug(f"Worker(thread) for grid #{res_gi} raised: {e}")
					if ok:
						success_count += 1
						debug(f"Grid #{res_gi} fully filled (thread) (time {dur:.3f}s)")
						for row in sol:
							debug(''.join(row))
					else:
						debug(f"Grid #{res_gi} cannot be fully filled (thread)")
					results[res_gi] = (ok, sol, dur)
	end_all = time.time()
	debug(f"\nTotal grids: {len(grids)}, successfully filled: {success_count}")
	debug(f"Total elapsed time: {end_all - start_all:.3f}s (workers={workers})")
	return success_count


# Update part_1 to use solve_grid_full and count fully solved grids

def final(shapes: Dict[str, List[str]], grids: List[dict]) -> int:
	"""Pour chaque grille demandée, tente de placer toutes les instances; si possible, incrémente le compteur de grilles résolues.
	Retourne le nombre de grilles pour lesquelles la solution complète a été trouvée.
	"""
	success_count = 0
	for gi, g in enumerate(grids):
		debug(f"\nTrying to fully fill grid #{gi} {g['width']}x{g['height']} counts={g['counts']}")
		ok, sol = solve_grid_full(g['width'], g['height'], shapes, g['counts'])
		if ok:
			success_count += 1
			debug(f"Grid #{gi} fully filled")
			for row in sol:
				debug(''.join(row))
		else:
			debug(f"Grid #{gi} cannot be fully filled")
	return success_count


if __name__ == "__main__":
	alpha = 'ABCDEF'
	shapes, grids = process_file("input.txt")
	debug(shapes, grids)
	# call part_1 with a number of workers (None or 1 = sequential)
	workers = min(4, os.cpu_count() or 1)
	print(f"Running with workers={workers}")
	print(f"result aoc day 12 - p1: {part_1(shapes, grids, workers=workers)}")  # print(f"result aoc day 12 - p2: {part_2(shapes, grids)}")
