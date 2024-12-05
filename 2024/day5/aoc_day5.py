import re
from typing import List


def process_file(filename: str) -> tuple[List, List]:
    with open(filename) as f:
        data = f.read().strip()
        rules = [(int(a), int(b)) for a, b in re.findall(r"(\d+)\|(\d+)", data)]
        updates = [list(map(int, line.split(',')))
                   for line in data.splitlines()
                   if ',' in line]
        return rules, updates


def part_1(rules, updates):
    def check_order(a, b):
        return any(x == a and y == b for x, y in rules)

    return sum(update[len(update) // 2]
               for update in updates
               if all(check_order(update[i], update[i + 1])
                      for i in range(len(update) - 1)))


def part_2(rules, updates):
    def check_order(a, b):
        return any(x == a and y == b for x, y in rules)

    def sort_by_rules(nums):
        n = len(nums)
        for i in range(n):
            for j in range(n - 1):
                if not check_order(nums[j], nums[j + 1]):
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
        return nums

    return sum(sort_by_rules(update.copy())[len(update) // 2]
               for update in updates
               if not all(check_order(update[i], update[i + 1])
                          for i in range(len(update) - 1)))


def main() -> None:
    rules, updates = process_file('input.txt')

    print(f"result aoc day 5 - p1: {part_1(rules, updates)}")
    print(f"result aoc day 5 - p2: {part_2(rules, updates)}")


if __name__ == "__main__":
    main()
