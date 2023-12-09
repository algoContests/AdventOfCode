import os
from collections import deque
from time import perf_counter
from typing import List

def update_grid(grid: List[str], path: List[str], start_pos: tuple):
    x, y = start_pos
    for _dir in path:
        grid[y][x] = _dir
        dx, dy = DIRS[_dir]
        x, y = x + dx, y + dy
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if grid[y][x] not in DIRS:
                grid[y][x] = '.'
    # return grid

def bfs(start: tuple, grid: List[str]) -> List[str]:
    print(start)
    queue = deque([(start, [None])])
    visited: set() = {start}
    while queue:
        pos, path = queue.popleft()
        x, y = pos
        for _dir, (dx, dy) in DIRS.items():
            X, Y = pos = x + dx, y + dy
            if not in_grid(*pos) or pos in visited:
                continue
            h = ord('a') if grid[y][x] == 'S' else ord('z') if grid[y][x] == 'E' else ord(grid[y][x])
            new_h = ord('z') if grid[Y][X] == 'E' else ord('a') if grid[Y][X] == 'S' else ord(grid[Y][X])
            if new_h > h + 1:
                continue
            if grid[Y][X] == 'E':
                return path
            # print(h, new_h)
            queue.append(((X, Y), path + [_dir]))
            visited.add(pos)

in_grid = lambda x, y: 0 <= x < WIDTH and 0 <= y < HEIGHT

DIRS = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}

TEST_MODE = False

if __name__ == "__main__":
    path_name = os.path.abspath(".")
    file_name = f'{path_name}/input_part1_test.txt' if TEST_MODE else f'{path_name}/input.txt'
    with open(file_name) as file:
        grid: List[int] = []
        if TEST_MODE:
            start_pos = (0, 0)
            WIDTH, HEIGHT = (8, 5)
        else:
            start_pos = (0, 20)
            WIDTH, HEIGHT = (80, 41)
        for line in file:
            line = line.replace('\n', '')
            grid.append(list(line))

        start = perf_counter()

        path = bfs(start_pos, grid)[1:]

        # for i, (x, y) in enumerate(path):
        #     grid[y][x] = str(i)

        print(f'{path} has length {len(path)}')
        # update grid with path
        update_grid(grid, path, start_pos)
        # print grid
        for i in range(HEIGHT):
            print(''.join([grid[i][j] for j in range(WIDTH)]))

        print(f'result part 1 = {len(path) + 1}')

        elapsed_time = (perf_counter() - start) * 1000
        print(f'elapsed time = {round(elapsed_time, 2)} ms')

        """
        v..v<<<<
        >v.vv<<^
        .>vv>E^^
        ..v>>>^^
        ..>>>>>^
        """