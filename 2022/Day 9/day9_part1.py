import os
from time import perf_counter


def move(x, y, _dir):
    dx, dy = DIRECTIONS[_dir]
    new_x, new_y = x + dx, y + dy
    return new_x, new_y

def move_to_head(tail, head):
    t_x, t_y = tail
    h_x, h_y = head
    if tail == head:
        return tail
    else:
        if t_x == h_x:
            if abs(h_y - t_y) == 1:
                return tail
            else:
                # move vertically
                t_y = h_y - 1 if h_y > t_y else t_y - 1
        elif t_y == h_y:
            if abs(h_x - t_x) == 1:
                return tail
            else:
                # move horizontally
                t_x = h_x - 1 if h_x > t_x else t_x - 1
        else:
            # move diagonally
            if abs(h_x - t_x) > 1:
                t_x = h_x - 1 if h_x > t_x else t_x - 1
                t_y = h_y
            elif abs(h_y - t_y) > 1:
                t_y = h_y - 1 if h_y > t_y else t_y - 1
                t_x = h_x
    return t_x, t_y

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        directions = []
        for line in file:
            _dir, step = line.split()
            directions.append((_dir, int(step)))

    start = perf_counter()

    DIRECTIONS = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
    s = (0, 0)
    head, tail = s, s
    visited = set()
    for _dir, step in directions:
        s = step
        while s > 0:
            head = move(*head, _dir)
            tail = move_to_head(tail, head)
            # print(f'head = {head} _dir = {_dir} -> tail = {tail}')
            visited.add(tail)
            s -= 1

    print(len(visited))

    elapsed_time = (perf_counter() - start) * 1000
    print(f'elapsed time = {round(elapsed_time, 2)} ms')