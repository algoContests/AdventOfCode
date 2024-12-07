import re
from itertools import product
from typing import List, Tuple


def process_file(filename: str) -> dict:
    """
    Processes the input file into a dictionary where:
    - Key: target value
    - Value: list of numbers
    """
    with open(filename) as f:
        return {int(k): list(map(int, v.split())) for k, v in (line.split(': ') for line in f)}


def evaluate_expression(nums: List[int], ops: tuple) -> int:
    result = nums[0]
    for i, op in enumerate(ops):
        n = nums[i + 1]
        result = int(str(result) + str(n)) if op == '|' else result + n if op == '+' else result * n
    return result


def part_1(data: dict) -> int:
    """
    Part 1: Determines the sum of target values where the equation is valid
    using only + and * operators.
    """
    return sum(
        target for target, nums in data.items()
        if any(
            evaluate_expression(nums, ops) == target
            for ops in product("+*", repeat=len(nums) - 1)
        )
    )


def part_2(data: dict) -> int:
    """
    Part 2: Determines the sum of target values where the equation is valid
    using +, *, and | operators.
    """
    return sum(
        target for target, nums in data.items()
        if any(
            evaluate_expression(nums, ops) == target
            for ops in product("+*|", repeat=len(nums) - 1)
        )
    )


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    data = process_file('input.txt')

    print(f"result aoc day 7 - p1: {part_1(data)}")
    print(f"result aoc day 7 - p2: {part_2(data)}")


if __name__ == "__main__":
    main()
