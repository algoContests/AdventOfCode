from functools import lru_cache


def process_file(filename: str) -> list[int]:
    """
    Processes the input file into a list of lists of integers representing the map.
    """
    with open(filename) as f:
        return list(map(int, f.read().strip().split()))


@lru_cache(maxsize=None)
def transform_stone(stone: int) -> list:
    """Transforms a single stone according to the rules."""
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        half = len(s) // 2
        return [int(s[:half]), int(s[half:])]
    else:
        return [stone * 2024]


def simulate_blinks(stones: list, blinks: int) -> int:
    """Simulates the stone transformations for the given number of blinks."""
    for _ in range(blinks):
        new_stones = []
        for stone in stones:
            new_stones.extend(transform_stone(stone))
        stones = new_stones
    return len(stones)


@lru_cache(None)
def dfs(stone, depth):
    if depth == 75:
        return 1
    if len(stone) % 2 == 0:
        counter = 0
        for nstone in (stone[:len(stone) // 2], stone[len(stone) // 2:]):
            while nstone[0] == "0" and len(nstone) > 1:
                nstone = nstone[1:]
            counter += dfs(nstone, depth + 1)
        return counter
    elif stone == "0":
        return dfs("1", depth + 1)
    else:
        return dfs(str(int(stone) * 2024), depth + 1)


def part_1(stones: list):
    return simulate_blinks(stones, 25)


def part_2(stones: list):
    # return simulate_blinks(stones, 75)
    return sum([dfs(str(stone), 0) for stone in stones])


def main() -> None:
    """
    Main function to run the program and display results for Part 1 and Part 2.
    """
    stones = process_file('input.txt')

    print(f"result aoc day 11 - p1: {part_1(stones)}")
    print(f"result aoc day 11 - p2: {part_2(stones)}")


if __name__ == "__main__":
    main()
