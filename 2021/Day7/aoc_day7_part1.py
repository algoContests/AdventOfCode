""" --- Day 7: The Treachery of Whales --- """
import math
import statistics

crabs = list(map(int, input().split(',')))

crabs.sort()
print(f'min: {min(crabs)} - max: {max(crabs)}')
print(crabs)

min_fuel = math.inf
for pos in crabs:
# for pos in range(max(crabs) + 1):
    fuel = sum([abs(p - pos) for p in crabs])
    if fuel < min_fuel:
        min_fuel = fuel
        best_pos = pos

mediane = (crabs[500] + crabs[501]) / 2
print(f'mediane = {mediane}')
print(f'other = {crabs[503]}')
print(f'{len(crabs)} crabs - median : {statistics.median(crabs)}')
print(f'best_pos = {best_pos} - min_fuel = {min_fuel}')

fuel = 0
for pos in crabs:
    fuel += abs(mediane - pos)

print(f'fuel = {fuel}')




