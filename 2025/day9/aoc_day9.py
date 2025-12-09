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
    """Compressed-coordinate implementation of part2: avoids building a large explicit grid.

    coords: list of (x,y) positions of red tiles.
    Returns largest rectangle area with red corners and all interior tiles red or green.
    """
    if not coords:
        return 0

    # unique sorted coordinate anchors
    xs = sorted(set(x for x, y in coords))
    ys = sorted(set(y for x, y in coords))
    min_x = min(xs); max_x = max(xs)
    min_y = min(ys); max_y = max(ys)

    # build Xs and Ys arrays including sentinel boundaries and x+1/y+1 to represent tiles
    Xs = sorted(set([min_x - 1, max_x + 1] + xs + [x + 1 for x in xs]))
    Ys = sorted(set([min_y - 1, max_y + 1] + ys + [y + 1 for y in ys]))

    widths = [Xs[i + 1] - Xs[i] for i in range(len(Xs) - 1)]
    heights = [Ys[i + 1] - Ys[i] for i in range(len(Ys) - 1)]
    w = len(widths); h = len(heights)

    x_to_idx = {X: i for i, X in enumerate(Xs)}
    y_to_idx = {Y: j for j, Y in enumerate(Ys)}

    def cx(x):
        return x_to_idx[x]
    def cy(y):
        return y_to_idx[y]

    reds = coords

    # neighbors along rows/cols
    neighbors = {p: set() for p in reds}
    by_row = {}
    by_col = {}
    for x, y in reds:
        by_row.setdefault(y, []).append(x)
        by_col.setdefault(x, []).append(y)
    for y, xs_row in by_row.items():
        xs_sorted = sorted(xs_row)
        for i, x in enumerate(xs_sorted):
            p = (x, y)
            if i > 0:
                neighbors[p].add((xs_sorted[i - 1], y))
            if i + 1 < len(xs_sorted):
                neighbors[p].add((xs_sorted[i + 1], y))
    for x, ys_col in by_col.items():
        ys_sorted = sorted(ys_col)
        for i, y in enumerate(ys_sorted):
            p = (x, y)
            if i > 0:
                neighbors[p].add((x, ys_sorted[i - 1]))
            if i + 1 < len(ys_sorted):
                neighbors[p].add((x, ys_sorted[i + 1]))

    # Build edges from ordered list: each red connects to the next in the list (wrap around)
    edges = set()
    # coords list wraps: connect reds[i] -> reds[(i+1)%n]
    n = len(reds)
    for i in range(n):
        a = reds[i]
        b = reds[(i + 1) % n]
        # ensure horizontal or vertical as guaranteed by problem
        if not (a[0] == b[0] or a[1] == b[1]):
            # fallback: if not aligned, skip (robustness)
            continue
        edges.add(tuple(sorted((a, b))))

    # allowed compressed cells
    allowed = [[False] * w for _ in range(h)]

    # mark red tile cells
    for x, y in reds:
        i = cx(x); j = cy(y)
        if 0 <= i < w and 0 <= j < h:
            allowed[j][i] = True

    # mark green edges in compressed indices
    for a, b in edges:
        (x1, y1), (x2, y2) = a, b
        if x1 == x2:
            i = cx(x1)
            j1 = cy(min(y1, y2))
            j2 = cy(max(y1, y2))
            for j in range(j1, j2 + 1):
                allowed[j][i] = True
        elif y1 == y2:
            j = cy(y1)
            i1 = cx(min(x1, x2))
            i2 = cx(max(x1, x2))
            for i in range(i1, i2 + 1):
                allowed[j][i] = True

    # flood-fill exterior on compressed grid
    from collections import deque
    vis = [[False] * w for _ in range(h)]
    q = deque()
    for i in range(w):
        if not allowed[0][i]:
            vis[0][i] = True; q.append((i, 0))
        if not allowed[h - 1][i]:
            vis[h - 1][i] = True; q.append((i, h - 1))
    for j in range(h):
        if not allowed[j][0]:
            vis[j][0] = True; q.append((0, j))
        if not allowed[j][w - 1]:
            vis[j][w - 1] = True; q.append((w - 1, j))
    while q:
        i, j = q.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < w and 0 <= nj < h and not vis[nj][ni] and not allowed[nj][ni]:
                vis[nj][ni] = True
                q.append((ni, nj))

    # interior cells are those not vis and not allowed
    for j in range(h):
        for i in range(w):
            if not allowed[j][i] and not vis[j][i]:
                allowed[j][i] = True

    # prefix sum of allowed areas (cell areas vary)
    ps = [[0] * (w + 1) for _ in range(h + 1)]
    for j in range(h):
        for i in range(w):
            cell_area = widths[i] * heights[j]
            ps[j + 1][i + 1] = ps[j][i + 1] + ps[j + 1][i] - ps[j][i] + (cell_area if allowed[j][i] else 0)

    def rect_area_sum(i1, j1, i2, j2):
        return ps[j2 + 1][i2 + 1] - ps[j1][i2 + 1] - ps[j2 + 1][i1] + ps[j1][i1]

    # search over all unordered pairs of red tiles as opposite corners
    best = 0
    n = len(reds)
    # Precompute global bounds for pruning
    max_x = max(x for x, y in reds)
    max_y = max(y for x, y in reds)
    min_x = min(x for x, y in reds)
    min_y = min(y for x, y in reds)
    for i in range(n):
        x_a, y_a = reds[i]
        for j in range(i + 1, n):
            x_b, y_b = reds[j]
            # form rectangle coordinates (inclusive)
            x1, x2 = (x_a, x_b) if x_a <= x_b else (x_b, x_a)
            y1, y2 = (y_a, y_b) if y_a <= y_b else (y_b, y_a)
            if x1 == x2 or y1 == y2:
                # degenerate (same row or same col) -> area zero in this context
                continue
            # quick global pruning: if max possible area with these mins cannot beat best
            possible_upper = (max_x - x1 + 1) * (max_y - y1 + 1)
            if possible_upper <= best:
                continue
            total_area = (x2 - x1 + 1) * (y2 - y1 + 1)
            if total_area <= best:
                continue
            i1 = cx(x1); i2 = cx(x2)
            j1 = cy(y1); j2 = cy(y2)
            allowed_area = rect_area_sum(i1, j1, i2, j2)
            if allowed_area == total_area:
                best = total_area
    return best


def main() -> None:
    coords = process_file('input.txt')
    print(f"result aoc day 9 - p1: {part_1(coords)}")
    print(f"result aoc day 9 - p2: {part_2(coords)}")


if __name__ == "__main__":
    main()
