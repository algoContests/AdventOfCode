import numpy as np

fishes = list(map(int, input().split(',')))
# fishes = np.array(list(map(int, input().split(','))))

fishes = {i: fish for i, fish in enumerate(fishes)}

print(fishes)

print(f'{len(fishes)} fish on day 1')

day = 0
while day < 120:
    new_fishes = {}
    # it = fishes.flat
    fish_count = len(fishes)
    #for i, fish in enumerate(fishes):
    for i, fish in fishes.items():
        if fish > 0:
            # fish -= 1
            fishes[i] -= 1
        else:
            # fish = 6
            fishes[i] = 6
            new_fishes[fish_count] = 8
            fish_count += 1
    #print(f'{len(new_fishes)} new fish day {day}')
    # new_fishes = np.array(new_fishes)
    # fishes = np.concatenate([fishes, new_fishes])
    fishes |= new_fishes
    day += 1

print(f'{len(fishes)} fish on day {day}')
