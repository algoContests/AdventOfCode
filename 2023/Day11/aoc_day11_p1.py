import math
import sys
from collections import deque
from typing import List


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


# Stupidos :-D
# def bfs_distance(g1, g2, grid):
#     w, h = len(grid[0]), len(grid)
#     queue = deque([(g1, 0)])
#     visited = set()
#     while queue:
#         g, d = queue.popleft()
#         if g == g2:
#             return d
#         visited.add(g)
#         x, y = g
#         for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
#                 queue.append(((nx, ny), d + 1))
#     return -1

transpose_matrix = lambda m: [[row[i] for row in m] for i in range(len(m[0]))]


def manhattan_distance(g1, g2):
    x1, y1 = g1
    x2, y2 = g2
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()
        lines = data.splitlines()

    w, h = len(lines[0]), len(lines)

    grid = []
    for i, line in enumerate(lines):
        debug(line)
        grid.append(list(line))
        if line.count('.') == w:
            grid.append(list(line))

    h = len(grid)
    a = transpose_matrix(grid)
    b = []
    for i, row in enumerate(a):
        b.append(row)
        if row.count('.') == h:
            b.append(row)
    grid = transpose_matrix(b)

    for row in grid:
        debug(''.join(row))

    w = len(grid[0])

    galaxies = [(x, y) for x in range(w) for y in range(h) if grid[y][x] == '#']
    debug(f'{len(galaxies)} galaxies - nombre de paires distinctes: {nombre_de_paires_distinctes(len(galaxies))}')
    a_faire = [(g1, g2) for g1 in galaxies for g2 in galaxies if g1 != g2]
    a_faire = suppress_duplicate_pairs(a_faire)
    debug(f'{len(a_faire)} distances à calculer')

    dist: int = 0
    for g1, g2 in a_faire:
        # print(f'Calculate distance {g1} -> {g2}')
        d = manhattan_distance(g1, g2, )
        # print(f'{g1} -> {g2} = {d}')
        dist += d

    print(dist)
