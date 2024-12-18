from collections import deque


def process_file(filename):
    with open(filename) as f:
        return [tuple(map(int, line.split(","))) for line in f]


def is_valid_position(x, y, forbidden):
    return 0 <= x < 71 and 0 <= y < 71 and (x, y) not in forbidden


def bfs(start, exit, forbidden):
    q = deque()
    q.appendleft((start[0], start[1], 0))
    visited = set()
    visited.add(start)

    while q:
        x, y, depth = q.pop()
        if (x, y) == exit:
            return True

        for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if is_valid_position(a, b, forbidden) and (a, b) not in visited:
                visited.add((a, b))
                q.appendleft((a, b, depth + 1))
    return False


def part_2(byte_positions):
    # Constants
    start = (0, 0)
    exit = (70, 70)
    forbidden = set()

    for i, byte in enumerate(byte_positions):
        forbidden.add(byte)
        if not bfs(start, exit, forbidden):
            return byte

    return "No blocking byte found"


def main():
    byte_positions = process_file('input.txt')

    blocking_byte = part_2(byte_positions)

    print("Coordinates of the first byte that will prevent the exit from being reachable:", f"{blocking_byte[0]},{blocking_byte[1]}")


if __name__ == "__main__":
    main()
