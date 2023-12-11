import math
import sys
from collections import deque
from typing import List

import numpy as np


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()


def nombre_de_paires_distinctes(n):
    if n < 2:
        return 0
    else:
        return math.factorial(n) // (2 * math.factorial(n - 2))


def suppress_duplicate_pairs(a_faire: List[tuple]):
    visited = set()
    new_a_faire = []
    for a, b in a_faire:
        if (a, b) in visited:
            continue
        visited.add((a, b))
        visited.add((b, a))
        new_a_faire.append((a, b))
    return new_a_faire


# transpose_matrix = lambda m: [[row[i] for row in m] for i in range(len(m[0]))]


def manhattan_distance(g1, g2):
    x1, y1 = g1
    x2, y2 = g2
    return abs(x1 - x2) + abs(y1 - y2)


def universe_distance(g1, g2, h_lines, v_lines):
    x1, y1 = g1
    x2, y2 = g2
    h_lines = [h for h in h_lines if y1 < h < y2] if y1 < y2 else [h for h in h_lines if y2 < h < y1] if y1 > y2 else []
    v_lines = [v for v in v_lines if x1 < v < x2] if x1 < x2 else [v for v in v_lines if x2 < v < x1] if x1 > x2 else []
    return manhattan_distance(g1, g2) + (len(h_lines) + len(v_lines)) * (expansion_factor - 1)


transpose_matrix = lambda m: [[row[i] for row in m] for i in range(len(m[0]))]

expansion_factor = 1000000

if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()
        lines = data.splitlines()

    w, h = len(lines[0]), len(lines)

    grid = []
    for i, line in enumerate(lines):
        debug(line)
        grid.append(list(line))

    tgrid = [*zip(*grid)]
    h_lines = [y for y in range(h) if grid[y].count('.') == w]
    v_lines = [x for x in range(w) if tgrid[x].count('.') == h]

    galaxies = [(x, y) for x in range(w) for y in range(h) if grid[y][x] == '#']
    debug(f'{len(galaxies)} galaxies - nombre de paires distinctes: {nombre_de_paires_distinctes(len(galaxies))}')
    a_faire = [(g1, g2) for g1 in galaxies for g2 in galaxies if g1 != g2]
    a_faire = suppress_duplicate_pairs(a_faire)
    debug(f'{len(a_faire)} distances à calculer')

    dist: int = 0
    for g1, g2 in a_faire:
        # print(f'Calculate distance {g1} -> {g2}')
        d = universe_distance(g1, g2, h_lines, v_lines)
        # print(f'{g1} -> {g2} = {d}')
        dist += d

    print(f'expansion factor = {expansion_factor} - résultat = {dist}')
