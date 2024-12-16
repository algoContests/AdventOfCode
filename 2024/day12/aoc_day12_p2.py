from collections import deque, defaultdict
from time import process_time


def process_file(filename: str) -> list[list[str]]:
    """
    Processes the input file into a list of lists of strings representing the map.
    """
    with open(filename) as f:
        return [list(line) for line in f.read().splitlines()]


def flood_fill(grid, i, j, visited):
    """
    Performs flood fill from position (i,j) and calculates area and perimeter.
    Returns tuple of (area, perimeter)
    """
    q = deque([(i, j)])
    visited.add((i, j))
    area = 0
    perimeter = 0
    edges = defaultdict(list)
    N = len(grid)

    while q:
        y, x = q.pop()
        area += 1
        for r, c in ((y + 1, x), (y - 1, x), (y, x - 1), (y, x + 1)):
            if not (0 <= r < N and 0 <= c < N) or grid[r][c] != grid[i][j]:
                edges[(r - y, c - x)].append((r, c))
            elif (r, c) not in visited:
                q.appendleft((r, c))
                visited.add((r, c))

    for edge_coords in edges.values():
        perimeter += len(edge_coords)
        for rr in range(len(edge_coords) - 1):
            r, c = edge_coords[rr]
            for rr1 in range(rr + 1, len(edge_coords)):
                y, x = edge_coords[rr1]
                if abs(r - y) + abs(c - x) == 1:
                    perimeter -= 1

    return area, perimeter


def part_2(grid):
    start_time = process_time()
    visited = set()
    total = 0
    N = len(grid)

    for i in range(N):
        for j in range(N):
            if (i, j) not in visited:
                area, perimeter = flood_fill(grid, i, j, visited)
                total += area * perimeter

    print(f"Time: {process_time() - start_time:.2f} seconds")
    return total


def main():
    grid = process_file('input.txt')

    print(f"result aoc day 15 - p2: {part_2(grid)}")


if __name__ == "__main__":
    main()
