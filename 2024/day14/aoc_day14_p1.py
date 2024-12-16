from functools import lru_cache

def process_file(filename: str) -> list[tuple]:
    """
    Processes the input file into a list of tuples representing the robots.
    """
    with open(filename) as f:
        robots = []
        for line in f:
            p_part, v_part = line.split()
            px, py = map(int, p_part[2:].split(","))
            vx, vy = map(int, v_part[2:].split(","))
            robots.append(((px, py), (vx, vy)))
        return robots


def part_1(robots):
    """ Calculate safety factor """
    # Dimensions of the grid
    WIDTH = 101
    HEIGHT = 103
    MID_X = 50
    MID_Y = 51

    # Simulate positions after 100 seconds
    counts = {"TL": 0, "TR": 0, "BL": 0, "BR": 0}  # Top-Left, Top-Right, etc.
    for (px, py), (vx, vy) in robots:
        x_new = (px + vx * 100) % WIDTH
        y_new = (py + vy * 100) % HEIGHT

        # Exclude robots on middle boundaries
        if x_new == MID_X or y_new == MID_Y:
            continue

        # Determine the quadrant
        if x_new < MID_X and y_new < MID_Y:
            counts["TL"] += 1
        elif x_new > MID_X and y_new < MID_Y:
            counts["TR"] += 1
        elif x_new < MID_X and y_new > MID_Y:
            counts["BL"] += 1
        elif x_new > MID_X and y_new > MID_Y:
            counts["BR"] += 1

    # Calculate safety factor
    safety_factor = counts["TL"] * counts["TR"] * counts["BL"] * counts["BR"]
    return safety_factor


def part_2(robots):
    """
    Find the fewest seconds for robots to form a compact pattern.
    """

    def calculate_positions(robots, time):
        """Calculate the positions of robots after a given time."""
        return [
            ((px + vx * time) % 101, (py + vy * time) % 103)
            for (px, py), (vx, vy) in robots
        ]

    def bounding_box(positions):
        """Calculate the bounding box size of the given positions."""
        min_x = min(pos[0] for pos in positions)
        max_x = max(pos[0] for pos in positions)
        min_y = min(pos[1] for pos in positions)
        max_y = max(pos[1] for pos in positions)
        return max_x - min_x + 1, max_y - min_y + 1

    min_area = float("inf")
    best_time = 0
    best_positions = []

    # Simulate until a pattern is formed
    for time in range(10000):  # Arbitrary large limit
        positions = calculate_positions(robots, time)
        width, height = bounding_box(positions)
        area = width * height

        # Check for minimum bounding box area
        if area < min_area:
            min_area = area
            best_time = time
            best_positions = positions

    # Display the pattern
    display_pattern(best_positions)
    return best_time


def display_pattern(positions):
    """Visualize the pattern formed by the robots."""
    grid = [["." for _ in range(101)] for _ in range(103)]
    for x, y in positions:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    data = process_file('input.txt')

    print(f"result aoc day 14 - p1: {part_1(data)}")


if __name__ == "__main__":
    main()
