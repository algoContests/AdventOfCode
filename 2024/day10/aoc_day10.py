from typing import List
from collections import deque


def process_file(filename: str) -> List[List[int]]:
    """
    Processes the input file into a list of lists of integers representing the map.
    """
    with open(filename) as f:
        return [list(map(int, line)) for line in f.read().splitlines()]


def in_grid(map_data, x, y):
    return 0 <= x < len(map_data) and 0 <= y < len(map_data[0])


def find_trailheads(map_data):
    trailheads = []
    for x in range(len(map_data)):
        for y in range(len(map_data[0])):
            if map_data[x][y] == 0:
                trailheads.append((x, y))
    return trailheads


def explore_trail(map_data, start):
    queue = deque([(start[0], start[1], 0)])
    visited = set()
    scores = 0

    while queue:
        x, y, height = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if map_data[x][y] == 9:
            scores += 1
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if in_grid(map_data, nx, ny) and (nx, ny) not in visited and map_data[nx][ny] == height + 1:
                queue.append((nx, ny, height + 1))
    return scores


def explore_trail_p2(map_data, start):
    queue = deque([(start[0], start[1], 0, [start])])
    trails = set()

    while queue:
        x, y, h, trail = queue.popleft()
        if tuple(trail) in trails: continue
        if map_data[x][y] == 9:
            trails.add(tuple(trail))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if in_grid(map_data, nx, ny) and map_data[nx][ny] == h + 1:
                queue.append((nx, ny, h + 1, trail + [(nx, ny)]))
    return len(trails)


def part_1(map_data):
    trailheads = find_trailheads(map_data)
    total_score = 0
    for trailhead in trailheads:
        total_score += explore_trail(map_data, trailhead)
    return total_score


def part_2(map_data):
    trailheads = find_trailheads(map_data)
    total_score = 0
    for trailhead in trailheads:
        total_score += explore_trail_p2(map_data, trailhead)
    return total_score


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    map_data = process_file('input.txt')

    print(f"result aoc day 10 - p1: {part_1(map_data)}")
    print(f"result aoc day 10 - p2: {part_2(map_data)}")


if __name__ == "__main__":
    main()
