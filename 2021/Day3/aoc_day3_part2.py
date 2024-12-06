""" --- Day 3: Binary Diagnostic --- Part 2 """
from copy import deepcopy

binary_numbers_input = []
while True:
    try:
        binary_number = list(map(int, input()))
        binary_numbers_input.append(binary_number)
    except EOFError:
        break

w = 12

i = 0
binary_numbers = deepcopy(binary_numbers_input)
while binary_numbers and i < w and len(binary_numbers) > 1:
    d = {0: 0, 1: 0}
    for binary_number in binary_numbers:
        if binary_number[i] == 0:
            d[0] += 1
        else:
            d[1] += 1
    digit = max(d.items(), key=lambda x: x[1])[0] if d[0] != d[1] else 1
    binary_numbers = [number for number in binary_numbers if number[i] == digit]
    i += 1

print(f'last digit used for oxygen rating: {i - 1}')

oxygen_rating = binary_numbers[0]
oxygen_rating = ''.join(map(str, oxygen_rating))
oxygen_rating = int(oxygen_rating, 2)

# print(oxygen_rating)

i = 0
binary_numbers = deepcopy(binary_numbers_input)
while binary_numbers and i < w and len(binary_numbers) > 1:
    d = {0: 0, 1: 0}
    for binary_number in binary_numbers:
        if binary_number[i] == 0:
            d[0] += 1
        else:
            d[1] += 1
    digit = min(d.items(), key=lambda x: x[1])[0] if d[0] != d[1] else 0
    binary_numbers = [number for number in binary_numbers if number[i] == digit]
    i += 1

print(f'last digit used for CO2 rating: {i - 1}')

CO2_scrubber = binary_numbers[0]
CO2_scrubber = ''.join(map(str, CO2_scrubber))
CO2_scrubber = int(CO2_scrubber, 2)

# print(CO2_scrubber)

life_support_rating = oxygen_rating * CO2_scrubber
# print(life_support_rating)
