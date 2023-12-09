import numpy as np
from collections import Counter

# fishes = list(map(int, input().split(',')))
inputs = np.array(list(map(int, input().split(','))))
print(inputs)

print(f'{len(inputs)} fish on day 1')

fishes = Counter()

for i, fish in enumerate(fishes):
    fishes[i] = fish

print(fishes)

day = 0
while day < 80:
    born_fishes = Counter()
    fishes_count = fishes.total()
    print(f'fish count = {fishes_count} - day {day}')
    for key, value in fishes.items():
        if value > 0:
            fishes[key] -= 1
        else:
            fishes[key] = 6
            born_fishes[fishes_count] = 8
            fishes_count += 1
    fishes |= born_fishes
    day += 1

print(f'{len(fishes)} fish on day {day}')
