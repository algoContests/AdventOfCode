""" --- Day 7: The Treachery of Whales ---
    Answer: best_pos = 478 - min_fuel = 101079875
    """
from copy import deepcopy

import math
import statistics

crabs = list(map(int, input().split(',')))

crabs.sort()
print(f'min: {min(crabs)} - max: {max(crabs)}')
print(crabs)

min_fuel = math.inf
for pos in range(max(crabs) + 1):
    c = crabs[:]
    fuel, step = 0, 1
    while len(set(c)) > 1:
        for i, p in enumerate(c):
            fuel += step if p != pos else 0
            if p < pos:
                c[i] += 1
            elif p > pos:
                c[i] -= 1
            # print(f'pos = {pos} - step = {step} - fuel = {fuel}')
        #print(f'c = {list(reversed(c))}')
        step += 1
    print(f'pos = {pos} - fuel = {fuel}')
    if fuel < min_fuel:
        min_fuel = fuel
        best_pos = pos

print(f'best_pos = {best_pos} - min_fuel = {min_fuel}')






