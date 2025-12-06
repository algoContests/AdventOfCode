import re
import numpy as np


def extract_numbers_with_alignement(lines):
    positions = [
        [(m.start(), m.end()) for m in re.finditer(r"\S+", line)]
        for line in lines
    ]
    col_bounds = [
        (min(s for s, _ in col), max(e for _, e in col))
        for col in zip(*positions)
    ]
    return [
        [line[start:end].ljust(end - start) for start, end in col_bounds]
        for line in lines
    ]


def process_file(filename):
    with open(filename, encoding="utf-8") as f:
        data = [line.rstrip("\n") for line in f]
    return extract_numbers_with_alignement(data[:-1]), data[-1].split()


def somme(numbers):
    return sum(int(''.join(word[i] for word in numbers if word[i] != ' '))
               for i in range(len(numbers[0])))


def prod(numbers):
    result = 1
    for i in range(len(numbers[0])):
        result *= int(''.join(word[i] for word in numbers if word[i] != ' '))
    return result


def part_2(numbers, operators):
    numbers = np.array(numbers, dtype=str).T
    return sum(somme(numbers[i]) if op == '+' else prod(numbers[i])
               for i, op in enumerate(operators))


def main():
    numbers, operators = process_file('input.txt')
    print(f"result aoc day 6 - p2: {part_2(numbers, operators)}")


if __name__ == "__main__":
    main()
