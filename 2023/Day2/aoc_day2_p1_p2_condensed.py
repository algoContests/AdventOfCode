import fileinput
import re

lines = list(map(lambda x: x.strip(), list(fileinput.input('input.txt'))))
day = 2
# code for both parts
result_part_1 = 0
result_part_2 = 0
for line in lines:
    # split the line to get the game id and sets
    game, sets = line.split(':')

    # for every color find every amount using regex and from them get the maximum
    red = [int(amount) for amount, _color in re.findall("(\d+) (red)", sets)]
    green = [int(amount) for amount, _color in re.findall("(\d+) (green)", sets)]
    blue = [int(amount) for amount, _color in re.findall("(\d+) (blue)", sets)]
    max_red, max_green, max_blue = max(red), max(green), max(blue)

    # part 1: check if the maximum of every color is smaller than the given numbers if so add the game ids to the result
    if max_red <= 12 and max_green <= 13 and max_blue <= 14:
        result_part_1 += int(re.findall("\d+", game)[0])

    # part 2: add the 'power' of all the maximum values
    result_part_2 += max_red * max_green * max_blue

# print the results
print(f"--- Day {day}: ---")
print(f"Part 1: {result_part_1}")
print(f"Part 2: {result_part_2}")
