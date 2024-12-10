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




def part_1(antennas, width, height) -> int:
    """Calculates all unique antinode positions in the map."""
    antinodes = set()

    # Use defaultdict to eliminate the need for setdefault
    by_frequency = defaultdict(list)
    for x, y, freq in antennas:
        by_frequency[freq].append((x, y))

    # Process each frequency group using combinations
    for positions in by_frequency.values():
        # Use combinations instead of nested loops
        for (x1, y1), (x2, y2) in combinations(positions, 2):
            # Midpoint check
            if not ((x1 + x2) & 1 or (y1 + y2) & 1):  # Using bitwise AND for modulo 2
                mx, my = (x1 + x2) >> 1, (y1 + y2) >> 1  # Using bit shift for division by 2
                antinodes.add((mx, my))

            # Calculate differences once
            dx, dy = x2 - x1, y2 - y1

            # Antinodes at double distance - unrolled loop
            ax1, ay1 = x2 + dx, y2 + dy
            if 0 <= ax1 < width and 0 <= ay1 < height:
                antinodes.add((ax1, ay1))

            ax2, ay2 = x2 - dx, y2 - dy
            if 0 <= ax2 < width and 0 <= ay2 < height:
                antinodes.add((ax2, ay2))

    return len(antinodes)


def part_1_old(antennas, width, height) -> int:
    """Calculates all unique antinode positions in the map."""
    antinodes = set()

    # Group antennas by frequency
    by_frequency = {}
    for x, y, freq in antennas:
        by_frequency.setdefault(freq, []).append((x, y))

    # Process each frequency group
    for freq, positions in by_frequency.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]

                # Midpoint and double distance checks
                dx, dy = x2 - x1, y2 - y1
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2

                if (x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0:  # Midpoint is integer
                    antinodes.add((mx, my))

                # Antinodes at double distance
                for k in (-1, 1):
                    ax, ay = x2 + k * dx, y2 + k * dy
                    if 0 <= ax < width and 0 <= ay < height:
                        antinodes.add((ax, ay))

    return len(antinodes)

def part_2(antennas, width, height) -> int:
    pass


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    antennas, width, height = process_file('input.txt')


    print(f"result aoc day 8 - p1: {part_1(antennas, width, height)}")
    print(f"result aoc day 8 - p2: {part_2(antennas, width, height)}")


if __name__ == "__main__":
    main()
