import fileinput
import re
from dataclasses import dataclass
from typing import List

lines = list(map(lambda x: x.strip(), list(fileinput.input('input.txt'))))

seeds: List[int] = list(map(int, re.findall(r'(\d+)', lines[0].split(':')[1])))
print(f'{len(seeds)} seeds')
# print(f'start seeds values part 1: {seeds}')
seeds: dict = {s: (s, 'seed') for s in seeds}

category: str = ''
for line in lines[1:]:
    numbers: List[int] = re.findall(r'(\d+)', line)
    if 'map' in line:
        category = line.split(':')[0]
    if numbers:
        dest, source, length = map(int, numbers)
        for k, (s, s_cat) in seeds.items():
            if source <= s <= source + length and s_cat != category:
                delta = s - source
                seeds[k] = (dest + delta, category)
        # print(f'{category}: {[dest, source, length]} -> new seeds values: {list(seeds.values())}')
# print(f'final seeds values: {list(seeds.values())}')
# too high: 1719006987
# good value: 462648396

result = min(seeds.values())
print(f'result part 1: {result}')