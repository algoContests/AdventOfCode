import re
from typing import List, Tuple


def process_file(filename: str) -> tuple[List, List]:
    with open(filename) as f:
        data = f.readlines()
        grid = []
        for i, line in enumerate(data):
            if '^' in line:
                guard_pos = line.index('^'), i
                line = line.replace('^', '.')
            grid.append(list(line.strip()))
        return grid, guard_pos


def part_1(grid, guard_pos):
    x, y = guard_pos
    visited = {guard_pos}
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    dir_idx = 0
    dx, dy = dirs[0]
    x, y = x + dx, y + dy

    while in_grid(x, y, grid):
        if grid[y][x] == '.':
            visited.add((x, y))
        else:
            x, y = x - dx, y - dy
            dir_idx = (dir_idx + 1) % 4
            dx, dy = dirs[dir_idx]
        x, y = x + dx, y + dy

    return len(visited)


def simulate_with_obstruction(grid: List[List[str]], guard_pos: Tuple[int, int], obstruction: Tuple[int, int]) -> bool:
    x, y = guard_pos
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    dir_idx = 0
    dx, dy = dirs[0]

    # Place obstruction
    grid[obstruction[1]][obstruction[0]] = '#'
    visited = set()

    while in_grid(x, y, grid):
        if grid[y][x] == '.':
            visited.add((x, y, dir_idx))
        else:
            dx, dy = dirs[dir_idx]
            x, y = x - dx, y - dy
            dir_idx = (dir_idx + 1) % 4
            dx, dy = dirs[dir_idx]
        x, y = x + dx, y + dy
        if (x, y, dir_idx) in visited:
            grid[obstruction[1]][obstruction[0]] = '.'
            return True
    grid[obstruction[1]][obstruction[0]] = '.'
    return False


def part_2(grid: List[List[str]], guard_pos: Tuple[int, int]) -> int:
    """
    Counts the number of possible positions where adding an obstruction causes the guard to get stuck in a loop.
    """
    return sum(
        simulate_with_obstruction(grid, guard_pos, (x, y))
        for y in range(len(grid))
        for x in range(len(grid[0]))
        if grid[y][x] == '.' and (x, y) != guard_pos
    )


in_grid = lambda x, y, grid: 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def main() -> None:
    grid, guard_pos = process_file('input.txt')

    print(f"result aoc day 6 - p1: {part_1(grid, guard_pos)}")
    print(f"result aoc day 6 - p2: {part_2(grid, guard_pos)}")


if __name__ == "__main__":
    main()
