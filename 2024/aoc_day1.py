from typing import List, Tuple, Any


def process_file(filename: str) -> list[Any]:
    with open(filename) as f:
        # Use list comprehension for faster list creation
        numbers = [(int(a), int(b)) for line in f
                   for a, b in [line.strip().split()]]
        return list(zip(*numbers))  # Unzip the pairs into two lists


def part_1(liste_1: List[int], liste_2: List[int]) -> int:
    """Calculate total distance using sorted lists."""
    return sum(abs(a - b) for a, b in zip(sorted(liste_1), sorted(liste_2)))


def part_2(l1: List[int], l2: List[int]) -> int:
    return sum(a * l2.count(a) for a in l1)


def main() -> None:
    l1, l2 = map(list, process_file('input.txt'))

    print(f"result aoc day 1 - p1: {part_1(l1, l2)}")
    print(f"result aoc day 1 - p2: {part_2(l1, l2)}")


if __name__ == "__main__":
    main()
