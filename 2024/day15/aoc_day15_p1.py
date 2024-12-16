from time import process_time


def process_file(filename: str) -> tuple:
    """
    Processes the input file into a list of lists of integers representing the map.
    """
    with open(filename) as f:
        map_str, moves_str = f.read().split('\n\n')
        warehouse_map = [list(line) for line in map_str.strip().split('\n')]
        moves = moves_str.replace('\n', '')
        return warehouse_map, moves


def find_robot(warehouse_map):
    return next(((x, y) for y, row in enumerate(warehouse_map)
                 for x, cell in enumerate(row) if cell == '@'), None)


def part_1(grid, moves):
    start_time = process_time()
    grid = [list(row) for row in grid]
    x, y = next((x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == '@')
    grid[y][x] = '.'

    delta = {'<': (-1, 0), '^': (0, -1), '>': (1, 0), 'v': (0, 1)}

    for d in moves:
        dx, dy = delta[d]
        r, c = y + dy, x + dx

        while grid[r][c] == 'O':
            r, c = r + dy, c + dx

        if grid[r][c] == '.':
            if dy:
                rng = range(min(r, y), max(r, y))
                if dy > 0: rng = reversed(range(min(r, y) + 1, max(r, y) + 1))
                for i in rng:
                    grid[i][c] = grid[i - 1 if dy > 0 else i + 1][c]
            if dx:
                rng = range(min(c, x), max(c, x))
                if dx > 0: rng = reversed(range(min(c, x) + 1, max(c, x) + 1))
                for i in rng:
                    grid[r][i] = grid[r][i - 1 if dx > 0 else i + 1]
            y, x = y + dy, x + dx

    score = sum(y * 100 + x for y, row in enumerate(grid) for x, c in enumerate(row) if c == 'O')
    print(f"Time: {process_time() - start_time:.2f} seconds")
    return score


def part_2(grid, moves):
    # Implementation for part 2
    pass


def main() -> None:
    grid, moves = process_file('input.txt')

    print(f"result aoc day 15 - p1: {part_1(grid, moves)}")


if __name__ == "__main__":
    main()
