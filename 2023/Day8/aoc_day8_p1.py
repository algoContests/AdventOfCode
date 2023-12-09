import re

import sys

from time import perf_counter


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()


if __name__ == "__main__":
    with open('input.txt') as f:
        lines = f.read().split("\n")

    # Input processing
    directions = list(lines[0])
    start = lines[2].split('=')[0].strip()

    rules: dict = {}
    for line in lines[2:]:
        node, dirs = line.split('=')
        left, right = re.findall(r'([A-Z]{3})', dirs)
        rules[node.strip()] = (left.strip(), right.strip())

    debug(f'{len(directions)} directions: {directions}')
    debug(rules)

    # Algorithm
    steps: int = 0
    current = 'AAA'
    while current != 'ZZZ':
        for _dir in directions:
            steps += 1
            current = rules[current][0] if _dir == 'L' else rules[current][1]
            if current == 'ZZZ':
                break

    print(steps)