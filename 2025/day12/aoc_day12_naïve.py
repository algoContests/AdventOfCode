import re
from typing import Dict, List, Tuple


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


def debug(shapes, grids):
	print("Shapes parsed:")
	for k, rows in shapes.items():
		print(f"{k}:")
		for r in rows:
			print(f"\t{r}")
	print('\nGrid requests:')
	for g in grids:
		print(f"{g['width']}x{g['height']}: {g['counts']}")


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
	"""Tente de placer toutes les instances demandées; retourne (True, grid) si une solution complète existe.
	"""
	alpha = 'ABCDEF'
	# Precompute rotations and offsets
	shape_types = []
	for idx, cnt in enumerate(counts):
		letter = alpha[idx]
		shape = shapes.get(letter)
		if not shape:
			shape_types.append({'letter': letter, 'rots': [], 'count': cnt})
			continue
		rots_raw = all_rotations(shape)
		rots = []
		seen = set()
		for r in rots_raw:
			key = tuple(r)
			if key in seen:
				continue
			seen.add(key)
			h = len(r)
			w = len(r[0]) if h > 0 else 0
			offsets, area = shape_offsets(r)
			rots.append({'w': w, 'h': h, 'offsets': offsets, 'shape': r})
		shape_types.append({'letter': letter, 'rots': rots, 'count': cnt})

	# Order types to reduce branching: ones with more instances first
	order = list(range(len(shape_types)))
	order.sort(key=lambda i: -shape_types[i]['count'])

	# build positions cache
	positions_cache = {}
	for st in shape_types:
		for rot in st['rots']:
			rkey = (rot['w'], rot['h'])
			if rkey not in positions_cache:
				positions_cache[rkey] = [(x, y) for y in range(0, height - rot['h'] + 1) for x in range(0, width - rot['w'] + 1)]

	grid = [['.' for _ in range(width)] for _ in range(height)]
	solution_grid = [['.' for _ in range(width)] for _ in range(height)]

	counts_ordered = [shape_types[i]['count'] for i in order]

	def can_place_offsets(offsets, x0, y0):
		for ox, oy in offsets:
			x = x0 + ox
			y = y0 + oy
			if x < 0 or y < 0 or x >= width or y >= height:
				return False
			if grid[y][x] != '.':
				return False
		return True

	def place(offsets, x0, y0, letter):
		for ox, oy in offsets:
			grid[y0 + oy][x0 + ox] = letter

	def unplace(offsets, x0, y0):
		for ox, oy in offsets:
			grid[y0 + oy][x0 + ox] = '.'

	# DFS that returns True when a full assignment found
	def dfs(idx):
		# if all types processed, check counts
		if idx == len(order):
			# if all counts zero, solution found
			if all(c == 0 for c in counts_ordered):
				for y in range(height):
					solution_grid[y] = grid[y].copy()
				return True
			else:
				return False
		# find next type with remaining >0
		si = idx
		# skip types with zero remaining
		while si < len(order) and counts_ordered[si] == 0:
			si += 1
		if si >= len(order):
			return dfs(len(order))
		# try to place one instance of this type
		type_idx = order[si]
		st = shape_types[type_idx]
		letter = st['letter']
		# if no rotations available but count>0 -> impossible
		if not st['rots'] and counts_ordered[si] > 0:
			return False
		# Try all rotations and positions
		for rot in st['rots']:
			pos_list = positions_cache.get((rot['w'], rot['h']), [])
			for (x0, y0) in pos_list:
				if can_place_offsets(rot['offsets'], x0, y0):
					place(rot['offsets'], x0, y0, letter)
					counts_ordered[si] -= 1
					# recurse on same idx (still may need to place more of same type)
					if dfs(si):
						return True
					# backtrack
					counts_ordered[si] += 1
					unplace(rot['offsets'], x0, y0)
		# If no placement leads to solution, cannot fulfill this type -> return False
		return False

	# start DFS from first ordered type
	ok = dfs(0)
	return ok, solution_grid


# Update part_1 to use solve_grid_full and count fully solved grids

def part_1(shapes: Dict[str, List[str]], grids: List[dict]) -> int:
	"""Pour chaque grille demandée, tente de placer toutes les instances; si possible, incrémente le compteur de grilles résolues.
	Retourne le nombre de grilles pour lesquelles la solution complète a été trouvée.
	"""
	success_count = 0
	for gi, g in enumerate(grids):
		print(f"\nTrying to fully fill grid #{gi} {g['width']}x{g['height']} counts={g['counts']}")
		ok, sol = solve_grid_full(g['width'], g['height'], shapes, g['counts'])
		if ok:
			success_count += 1
			print(f"Grid #{gi} fully filled")
			for row in sol:
				print(''.join(row))
		else:
			print(f"Grid #{gi} cannot be fully filled")
	return success_count


if __name__ == "__main__":
	alpha = 'ABCDEF'
	shapes, grids = process_file("input.txt")
	debug(shapes, grids)
	print(f"result aoc day 12 - p1: {part_1(shapes, grids)}")
	# print(f"result aoc day 12 - p2: {part_2(shapes, grids)}")
