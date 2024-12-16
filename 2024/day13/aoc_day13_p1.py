import re
from collections import deque


def process_file(filename: str) -> list[dict]:
    """Processes the input file into a list of dictionaries."""
    pattern = r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)'
    with open(filename) as f:
        return [{'A': (int(m.group(1)), int(m.group(2))),
                 'B': (int(m.group(3)), int(m.group(4))),
                 'prize': (int(m.group(5)), int(m.group(6)))}
                for m in re.finditer(pattern, f.read())]


def find_min_tokens(Ax, Ay, Bx, By, Px, Py):
    min_tokens = float('inf')
    found_solution = False

    for a in range(101):
        for b in range(101):
            # Check if the combination aligns with the prize
            if a * Ax + b * Bx == Px and a * Ay + b * By == Py:
                found_solution = True
                # Calculate the token cost
                cost = 3 * a + b
                min_tokens = min(min_tokens, cost)

    return min_tokens if found_solution else None


def solve_claw_problem(data: list[dict]):
    total_tokens = 0
    prizes_won = 0

    for machine in data:
        Ax, Ay = machine['A']
        Bx, By = machine['B']
        Px, Py = machine['prize']

        # Find the minimum tokens needed for this machine
        min_tokens = find_min_tokens(Ax, Ay, Bx, By, Px, Py)

        if min_tokens is not None:
            prizes_won += 1
            total_tokens += min_tokens

    return prizes_won, total_tokens


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    data = process_file('input.txt')

    # Solve part 1
    prizes_won, total_tokens = solve_claw_problem(data)
    print(f"result aoc day 13 - p1: {total_tokens}")


if __name__ == "__main__":
    main()
