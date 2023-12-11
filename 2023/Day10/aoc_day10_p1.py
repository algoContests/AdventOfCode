import sys, re
from collections import deque

from typing import List


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()
        lines = data.splitlines()
        grid = []
        for line in lines:
            if 'S' in line:
                start = (line.index('S'), lines.index(line))
                line = line.replace('S', 'a')
            grid.append(list(line))

        #print(lines)
        for line in grid:
            print(line)

        """
            | is a vertical pipe connecting north and south.
            - is a horizontal pipe connecting east and west.
            L is a 90-degree bend connecting north and east.
            J is a 90-degree bend connecting north and west.
            7 is a 90-degree bend connecting south and west.
            F is a 90-degree bend connecting south and east.
        """
        possible_dirs = {'a': ('E', 'S', 'N', 'W'), 'F': ('E', 'S'), '|': ('N', 'S'), '-': ('W', 'E'), 'L': ('N', 'E'), 'J': ('N', 'W'), '7': ('S', 'W')}
        dirs = {'E':  (1, 0), 'S': (0, 1), 'W': (-1, 0), 'N': (0, -1)}
        geos = ['E', 'S', 'W', 'N']
        reverse_geos = ['W', 'N', 'E', 'S']
        w, h = len(grid[0]), len(grid)

        """
            .....
            .S-7.
            .|.|.
            .L-J.
            .....
        """
        def get_moves(pos):
            x, y = pos
            moves = []
            for _dir, (dx, dy) in dirs.items():
                from_cell_value = grid[y][x]
                if _dir not in possible_dirs[from_cell_value]:
                    continue
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h:
                    continue
                to_cell_value = grid[ny][nx]
                if to_cell_value == '.':
                    continue
                opposite_dir = reverse_geos[geos.index(_dir)]
                if opposite_dir not in possible_dirs[to_cell_value]:
                    continue
                moves.append((nx, ny))
            return moves

        moves = get_moves(start)
        path = [start]
        next = moves[0]
        visited = {start, next}
        while True:
            if next == start:
                break
            # debug(next)
            moves = [m for m in get_moves(next) if m not in visited]
            if not moves:
                break
            next = moves[0]
            path.append(next)
            visited.add(next)

        print(len(path) // 2 + 1)



