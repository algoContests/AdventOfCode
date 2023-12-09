import fileinput
import re
from dataclasses import dataclass
from typing import List


@dataclass
class PartNumber:
    x1: int
    x2: int
    y: int
    value: int

    def belongs_to(self, s: tuple) -> bool:
        part_positions: List[tuple] = [(x, self.y) for x in range(self.x1, self.x2 + 1)]
        x, y = s
        for X, Y in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1):
            if not in_grid(X, Y):
                continue
            if (X, Y) in part_positions:
                return True
        return False

lines = list(map(lambda x: x.strip(), list(fileinput.input('input.txt'))))
in_grid = lambda x, y: 0 <= x < width and 0 <= y < height

width, height = len(lines[0]), len(lines)

part_numbers: List[PartNumber] = []
symbols: List[tuple] = []
for i, line in enumerate(lines):
    decimal_pattern = re.compile(r'\d+')
    # numbers = re.findall("(\d+)", line)
    matches = [(match.start(), match.end()) for match in re.finditer(decimal_pattern, line)]
    for start, end in matches:
        part_numbers.append(PartNumber(start, end - 1, i, int(line[start:end])))
    # non_alpha_numeric_pattern = re.compile(r'\W')
    non_alpha_numeric_pattern = re.compile(r'[^a-zA-Z0-9_.]')
    matches = [match.start() for match in re.finditer(non_alpha_numeric_pattern, line)]
    for start in matches:
        symbols.append((start, i))

# Part 1
missing_pn: List[PartNumber] = []
gears: List[int] = []
for y in range(len(lines)):
    for s in symbols:
        if s[1] == y:
            neighbors: List[PartNumber] = [pn for pn in part_numbers if 0 <= pn.y <= y + 1 and pn.belongs_to(s)]
            missing_pn += neighbors
            if len(neighbors) == 2:
                gears.append(neighbors[0].value * neighbors[1].value)

result = sum([pn.value for pn in missing_pn])
print('part 1: ', result)

# part 2
result = sum(gears)
print('part 2: ', result)
