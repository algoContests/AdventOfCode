import re


def process_file(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def part_1(memory: str) -> int:
    # Regular expression to find valid 'mul' instructions
    pattern = r"mul\((\d+),(\d+)\)"

    # Find all matches in the memory string
    matches = re.findall(pattern, memory)

    # Calculate the sum of results
    return sum(int(a) * int(b) for a, b in matches)


def part_2(memory: str):
    pattern = re.compile(r'(?:do\(\)|don\'t\(\))|mul\((\d+),(\d+)\)')
    total = 0
    enabled = True

    for m in pattern.finditer(memory):
        if m.group(1) is None:
            enabled = m.group(0) == "do()"
        elif enabled:
            total += int(m.group(1)) * int(m.group(2))

    return total


def main() -> None:
    memory: str = process_file('input.txt')

    print(f"result aoc day 3 - p1: {part_1(memory)}")
    print(f"result aoc day 3 - p2: {part_2(memory)}")


if __name__ == "__main__":
    main()
