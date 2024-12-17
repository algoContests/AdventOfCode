import heapq
from time import process_time


def process_file(filename: str) -> tuple:
    """
     Parse the maze and find start and end positions
    """
    with open(filename) as f:
        grid = []
        start = end = None
        for y, line in enumerate(f.read().splitlines()):
            grid.append(line)
            for x, char in enumerate(line):
                if char == 'S':
                    start = (x, y)
                elif char == 'E':
                    end = (x, y)
        return grid, start, end


def is_valid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != '#'


def part_1(grid, start, end):

    # Directions: (dx, dy, direction)
    directions = [(1, 0, 'E'), (0, 1, 'S'), (-1, 0, 'W'), (0, -1, 'N')]
    direction_map = {d: i for i, d in enumerate(['E', 'S', 'W', 'N'])}

    # Priority queue: (score, x, y, direction index)
    pq = [(0, start[0], start[1], 0)]  # Starting facing East
    visited = set()

    while pq:
        score, x, y, dir_idx = heapq.heappop(pq)

        if (x, y, dir_idx) in visited:
            continue
        visited.add((x, y, dir_idx))

        if (x, y) == end:
            return score  # Found the end with the lowest score

        # Try moving forward
        dx, dy, _ = directions[dir_idx]
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, grid):
            heapq.heappush(pq, (score + 1, nx, ny, dir_idx))

        # Try turning (clockwise and counterclockwise)
        for turn in [-1, 1]:
            new_dir_idx = (dir_idx + turn) % 4
            heapq.heappush(pq, (score + 1000, x, y, new_dir_idx))



def main() -> None:
    # Parse the maze and find start and end positions
    grid, start, end = process_file('input.txt')

    print(f"result aoc day 16 - p1: {part_1(grid, start, end)}")


if __name__ == "__main__":
    main()
