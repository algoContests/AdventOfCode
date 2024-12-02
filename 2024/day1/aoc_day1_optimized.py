from typing import List, Tuple
from heapq import heapify, heappop


def process_file(filename: str) -> tuple:
    """Process file and return two sorted lists of integers."""
    with open(filename) as f:
        # Use list comprehension for faster list creation
        numbers = [(int(a), int(b)) for line in f
                   for a, b in [line.strip().split()]]
        return tuple(map(list, zip(*numbers)))  # Unzip the pairs into two lists


def part_1_optimized(liste_1: List[int], liste_2: List[int]) -> int:
    """Calculate total distance using heap for efficient minimum finding."""
    # Convert lists to heaps for O(1) min operations
    l1, l2 = [*liste_1], [*liste_2]
    heapify(l1)
    heapify(l2)
    distance: int = 0
    # Process all elements using heappop which is O(log n)
    while l1:
        distance += abs(heappop(l1) - heappop(l2))
    return distance

def part_1(liste_1: List[int], liste_2: List[int]) -> int:
    """Calculate total distance using sorted lists."""
    return sum(abs(a - b) for a, b in zip(sorted(liste_1), sorted(liste_2)))


def part_2(l1: List[int], l2: List[int]) -> int:
    return sum(a * l2.count(a) for a in l1)


def main() -> None:
    l1, l2 = process_file('input.txt')
    print(f"result aoc day 1 - p1: {part_1(l1, l2)}")
    print(f"result aoc day 1 - p2: {part_2(l1, l2)}")


if __name__ == "__main__":
    main()
