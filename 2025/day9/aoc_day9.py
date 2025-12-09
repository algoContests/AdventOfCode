import math
from typing import Any, List, Tuple


def process_file(filename: str) -> list[tuple[int, ...]]:
    coords = []
    with open(filename) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            parts = [p.strip() for p in s.split(',') if p.strip()]
            if len(parts) >= 2:
                coords.append((int(parts[0]), int(parts[1])))
    return coords


def build_enclosing_grid(coords: List[Tuple[int, int]], margin: int = 0) -> List[List[str]]:
    """Construit une grille minimale ('.' / '#') qui englobe toutes les coordonnées fournies.

    Retourne la grille avec les coordonnées translatées de sorte que la plus petite
    coordonnée x et y deviennent (0,0) dans la grille.
    """
    if not coords:
        return []
    min_x = min(x for x, y in coords) - margin
    min_y = min(y for x, y in coords) - margin
    max_x = max(x for x, y in coords) + margin
    max_y = max(y for x, y in coords) + margin

    w = max_x - min_x + 1
    h = max_y - min_y + 1
    grid: List[List[str]] = [["." for _ in range(w)] for _ in range(h)]
    for x, y in coords:
        grid[y - min_y][x - min_x] = '#'
    return grid


def part_1(reds: List[List[str]]) -> int:
    # collect (x,y) coordinates of red tiles (#). x=index in line, y=line index
    # red_tiles: List[Tuple[int, int]] = [(i, j) for j, line in enumerate(grid) for i, t in enumerate(line) if t == '#']
    # area should count tiles inclusively: width = X - x + 1, height = Y - y + 1
    surfaces = [(X - x + 1) * (Y - y + 1) for (x, y) in reds for (X, Y) in reds if X > x and Y > y]
    return max(surfaces) if surfaces else 0


def part_2(coords: List[Tuple[int, int]]) -> int:
    if not coords:
        return 0

    import numpy as np
    from collections import deque
    import itertools

    xs = sorted({x for x, _ in coords})
    ys = sorted({y for _, y in coords})
    Xs = sorted({min(xs) - 1, max(xs) + 1} | set(xs) | {x + 1 for x in xs})
    Ys = sorted({min(ys) - 1, max(ys) + 1} | set(ys) | {y + 1 for y in ys})

    widths = np.array([Xs[i + 1] - Xs[i] for i in range(len(Xs) - 1)], dtype=np.int64)
    heights = np.array([Ys[j + 1] - Ys[j] for j in range(len(Ys) - 1)], dtype=np.int64)
    x_idx = {X: i for i, X in enumerate(Xs)}
    y_idx = {Y: j for j, Y in enumerate(Ys)}
    w, h = len(widths), len(heights)

    # allowed mask
    allowed = np.zeros((h, w), dtype=bool)
    for x, y in coords:
        allowed[y_idx[y], x_idx[x]] = True

    # draw cycle edges (green segments)
    n = len(coords)
    for i in range(n):
        (x1, y1), (x2, y2) = coords[i], coords[(i + 1) % n]
        if x1 == x2:
            ci = x_idx[x1]; j1, j2 = y_idx[min(y1, y2)], y_idx[max(y1, y2)]
            allowed[j1:j2+1, ci] = True
        elif y1 == y2:
            rj = y_idx[y1]; i1, i2 = x_idx[min(x1, x2)], x_idx[max(x1, x2)]
            allowed[rj, i1:i2+1] = True

    # flood-fill exterior to identify interior cells
    vis = np.zeros((h, w), dtype=bool)
    q = deque()
    # border enqueue
    for i in range(w):
        if not allowed[0, i]: vis[0, i] = True; q.append((i, 0))
        if not allowed[h - 1, i]: vis[h - 1, i] = True; q.append((i, h - 1))
    for j in range(h):
        if not allowed[j, 0]: vis[j, 0] = True; q.append((0, j))
        if not allowed[j, w - 1]: vis[j, w - 1] = True; q.append((w - 1, j))
    while q:
        i, j = q.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < w and 0 <= nj < h and not vis[nj, ni] and not allowed[nj, ni]:
                vis[nj, ni] = True
                q.append((ni, nj))
    # interior cells become allowed
    allowed[~vis & ~allowed] = True

    # prefix sum of allowed * cell_area using numpy
    cell_area = (heights.reshape(-1, 1) * widths.reshape(1, -1)).astype(np.int64)
    allowed_area = (allowed * cell_area)
    cs = allowed_area.cumsum(axis=0).cumsum(axis=1)
    ps = np.zeros((h + 1, w + 1), dtype=np.int64)
    ps[1:, 1:] = cs

    def rect_sum(i1, j1, i2, j2):
        return int(ps[j2 + 1, i2 + 1] - ps[j1, i2 + 1] - ps[j2 + 1, i1] + ps[j1, i1])

    # test pairs of red tiles
    best = 0
    max_x = max(x for x, _ in coords)
    max_y = max(y for _, y in coords)
    for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
        lx, rx = (x1, x2) if x1 <= x2 else (x2, x1)
        ly, ry = (y1, y2) if y1 <= y2 else (y2, y1)
        if lx == rx or ly == ry:
            continue
        area = (rx - lx + 1) * (ry - ly + 1)
        if area <= best:
            continue
        if (max_x - lx + 1) * (max_y - ly + 1) <= best:
            continue
        i1, i2 = x_idx[lx], x_idx[rx]
        j1, j2 = y_idx[ly], y_idx[ry]
        if rect_sum(i1, j1, i2, j2) == area:
            best = area
    return best


def main() -> None:
    coords = process_file('input.txt')
    print(f"result aoc day 9 - p1: {part_1(coords)}")
    print(f"result aoc day 9 - p2: {part_2(coords)}")


if __name__ == "__main__":
    main()
