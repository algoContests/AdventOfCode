import numpy as np
from collections import Counter

# fishes = list(map(int, input().split(',')))
inputs = np.array(list(map(int, input().split(','))))


print(inputs)

print(f'{len(inputs)} fish on day 1')

fishes = Counter()

for i, fish in enumerate(fishes):
    fishes[i] = fish

day = 0
while day < 80:
    it = fishes.flat
    born_fishes = []
    with np.nditer(fishes, op_flags=['readwrite']) as it:
        for fish in it:
            if fish > 0:
                fish -= 1
            else:
                fish = 6
                born_fishes.append(fish)
    born_fishes = np.array(born_fishes)
    fishes = np.concatenate([fishes, born_fishes])
    day += 1

print(f'{len(fishes)} fish on day {day}')
