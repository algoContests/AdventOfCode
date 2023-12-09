import fileinput
import re
from typing import List

lines = list(map(lambda x: x.strip(), list(fileinput.input('input.txt'))))

# part 1

max_cubes = {'red': 12, 'green': 13, 'blue': 14}
possible_games: List[int] = []

for i, line in enumerate(lines):
    print(line)
    game_sets = line.split(':')[1]
    game = game_sets.split(";")
    # game_no = int(game_no.split()[1])
    amount_dict: dict = {'red': 0, 'green': 0, 'blue': 0}
    possible = True
    for partie in game:
        curr = partie.split(",")
        for elt in curr:
            e = elt.strip().split()
            amount, color = int(e[0]), e[1]
            if amount > max_cubes[color] and possible:
                possible = False
                break
        if not possible:
            break
    if not possible:
        continue
    possible_games.append(i + 1)
    # possible_games.append(game_no)

print(possible_games)
print(sum(possible_games))

