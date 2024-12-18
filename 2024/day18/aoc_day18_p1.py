import heapq


def process_file(filename):
    with open(filename) as f:
        return [tuple(map(int, line.split(","))) for line in f]


def simulate_bytes(memory_space, byte_positions, num_bytes):
    for x, y in byte_positions[:num_bytes]:
        memory_space[y][x] = '#'


def is_valid_position(x, y, memory_space):
    if 0 <= x < len(memory_space[0]) and 0 <= y < len(memory_space):
        return memory_space[y][x] != '#'
    return False


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def part_1(byte_positions):
    from collections import deque

    # Constants
    N = 1024
    W = 71
    start = (0, 0)
    exit = (W - 1, W - 1)

    # Initialize queue and forbidden set
    q = deque()
    q.appendleft((0, 0, 0))
    forbidden = {start}

    # Add byte positions to forbidden set (simulating 25 bytes instead of 1024 for simplicity)
    for i in range(min(N, len(byte_positions))):
        forbidden.add(byte_positions[i])

    # A* search algorithm
    while q:
        x, y, depth = q.pop()
        if (x, y) == exit:
            return depth

        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= a < W and 0 <= b < W and (a, b) not in forbidden:
                forbidden.add((a, b))
                q.appendleft((a, b, depth + 1))
    else:
        return "No path found to reach the exit."



def main():
    byte_positions = process_file('input.txt')

    min_steps = part_1(byte_positions)

    print("Minimum number of steps to reach the exit:", min_steps)


if __name__ == "__main__":
    main()
