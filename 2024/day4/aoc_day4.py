import re
from typing import List


def process_file(filename: str) -> List[str]:
    with open(filename) as f:
        return f.read().splitlines()


def part_1(grid: List[str]):
    rows, cols = len(grid), len(grid[0])
    word = "XMAS"

    def check(x, y, dx, dy):
        return all(0 <= x + i * dx < cols and 0 <= y + i * dy < cols and
                   grid[y + i * dy][x + i * dx] == word[i] for i in range(len(word)))

    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    return sum(check(x, y, dx, dy)
               for y in range(rows)
               for x in range(cols)
               for dx, dy in dirs)


def part_2(grid):
    def check(x, y):
        return (grid[y][x] == "A" and
                set(grid[y + dy][x + dx] for dx, dy in [(-1, 1), (1, -1)]) == {"M", "S"} and
                set(grid[y + dy][x + dx] for dx, dy in [(-1, -1), (1, 1)]) == {"M", "S"})

    return sum(check(x, y)
               for y in range(1, len(grid) - 1)
               for x in range(1, len(grid[0]) - 1))


def main() -> None:
    word_search: List[str] = process_file('input.txt')

    print(f"result aoc day 4 - p1: {part_1(word_search)}")
    print(f"result aoc day 4 - p2: {part_2(word_search)}")


if __name__ == "__main__":
    main()
