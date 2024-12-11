import math
from collections import defaultdict
from itertools import combinations


def process_file(filename: str) -> tuple:
    """
    Processes the input file into a dictionary where:
    - Key: target value
    - Value: list of numbers
    """
    with open(filename) as f:
        data = f.read().splitlines()
        # Map dimensions
        width, height = len(data[0]), len(data)
        """Parses the input map into a list of antenna positions and frequencies."""
        antennas = []
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char != '.':
                    antennas.append((x, y, char))
        return antennas, width, height


def part_1(antennas, width, height):
    antinodes = set()
    for i, (x1, y1, f1) in enumerate(antennas):
        for x2, y2, f2 in antennas[i + 1:]:
            if f1 == f2:
                dx, dy = x2 - x1, y2 - y1
                # Midpoint
                mx, my = x1 + dx / 2, y1 + dy / 2
                if mx.is_integer() and my.is_integer():
                    if 0 <= (mx := int(mx)) < width and 0 <= (my := int(my)) < height:
                        antinodes.add((mx, my))
                # Double distance points
                for x, y in [(x2 + dx, y2 + dy), (x1 - dx, y1 - dy)]:
                    if 0 <= x < width and 0 <= y < height:
                        antinodes.add((int(x), int(y)))
    return len(antinodes)


def part_2(antennas, width, height):
    antinodes = set()
    freq_groups = {}
    for x, y, f in antennas:
        freq_groups.setdefault(f, []).append((x, y))

    for points in freq_groups.values():
        if len(points) < 2:
            continue

        for i, (x1, y1) in enumerate(points):
            if 0 <= x1 < width and 0 <= y1 < height:
                antinodes.add((int(x1), int(y1)))

            for x2, y2 in points[i + 1:]:
                dx, dy = x2 - x1, y2 - y1
                if dx or dy:
                    gcd = abs(math.gcd(dx, dy)) if dy else abs(dx)
                    dx, dy = dx // gcd, dy // gcd

                    for direction in (1, -1):
                        x, y = x1, y1
                        while 0 <= x < width and 0 <= y < height:
                            antinodes.add((int(x), int(y)))
                            x += dx * direction
                            y += dy * direction

    return len(antinodes)


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    antennas, width, height = process_file('input.txt')

    print(f"result aoc day 8 - p1: {part_1(antennas, width, height)}")
    print(f"result aoc day 8 - p2: {part_2(antennas, width, height)}")


if __name__ == "__main__":
    main()
