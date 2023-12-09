import fileinput
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Seed:
    s: int
    x: int
    cat: int = -1

categories: List[str] = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                         'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']

lines = list(map(lambda x: x.strip(), list(fileinput.input('input.txt'))))

seeds: List[int] = list(map(int, re.findall(r'(\d+)', lines[0].split(':')[1])))
print(f'width = {len(seeds)}')

seeds_part2 = set()
for i in range(len(seeds) // 2) :
    start, end = seeds[2*i], seeds[2*i] + seeds[2*i+1]
    seeds_part2 |= set(range(start, end + 1))

print(len(seeds_part2))
# seeds: List[Seed] = [Seed(s=s, x=s) for s in seeds_part2]

exit(0)

category_idx: int = -1
for line in lines[1:]:
    numbers: List[int] = re.findall(r'(\d+)', line)
    if 'map' in line:
        category_idx: int = categories.index(line.split(' ')[0])
        print(f'process new category -> {categories[category_idx]}')
    if numbers:
        dest, source, length = map(int, numbers)
        for s in seeds:
            if s.cat != category_idx and source <= s.x <= source + length:
                s.x, s.cat = dest + s.x - source, category_idx

result = min(seeds, key=lambda s: s.x)
print(f'result: {result.x}')