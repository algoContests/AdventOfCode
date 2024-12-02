from typing import Any, List

import numpy as np


def process_file(filename: str) -> list[Any]:
    with open(filename) as f:
        return [list(map(int, line.split())) for line in f]


def is_safe(report: List[int]) -> bool:
    """
    Determines if a report is safe based on two conditions:
    1. Levels are either all increasing or all decreasing.
    2. Any two adjacent levels differ by at least 1 and at most 3.
    """
    # differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    differences = np.diff(report)

    # Check if all differences are within the range [-3, -1] (decreasing) or [1, 3] (increasing)
    return all(-3 <= d <= -1 for d in differences) or all(1 <= d <= 3 for d in differences)


def part_1(numbers: List[List[int]]) -> int:
    return len([report for report in numbers if is_safe(report)])


def check_with_dampener(report: List[int]) -> bool:
    """
    Checks if a report can be made safe by removing a single level.
    """
    return any(is_safe(np.delete(report, i)) for i in range(len(report)))


def part_2(numbers: List[List[int]]) -> int:
    return len([report for report in numbers if is_safe(report) or check_with_dampener(report)])


def main() -> None:
    numbers = process_file('input.txt')

    print(f"result aoc day 1 - p1: {part_1(numbers)}")
    print(f"result aoc day 1 - p2: {part_2(numbers)}")


if __name__ == "__main__":
    main()
