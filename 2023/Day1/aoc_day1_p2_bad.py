import re
from collections import deque
from typing import Tuple, List


def trouver_occurrences_positions_re(chaine_a_chercher, chaine_source):
    pattern = re.compile(re.escape(chaine_a_chercher))
    positions = [match.start() for match in pattern.finditer(chaine_source)]
    return positions


def trouver_occurrences_positions_find(chaine_a_chercher, chaine_source):
    positions = []
    index = chaine_source.find(chaine_a_chercher)
    while index != -1:
        positions.append(index)
        index = chaine_source.find(chaine_a_chercher, index + 1)
    return positions


def remplacer_occurrences(chaine_a_remplacer, chaine_de_remplacement, chaine_source):
    pattern = re.compile(re.escape(chaine_a_remplacer))
    nouvelle_chaine = pattern.sub(chaine_de_remplacement, chaine_source)
    return nouvelle_chaine


def format(line: str) -> str:
    positions: List[tuple[str, int]] = []
    digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', "eight", "nine"]
    for d in digits:
        number: int = digits.index(d) + 1
        for position in trouver_occurrences_positions_find(d, line):
            positions.append((str(number), position))
    c_digits = filter(lambda x: x.isdigit(), line)
    positions += [(c, pos) for c in c_digits for pos in trouver_occurrences_positions_find(c, line) if c.isdigit()]
    positions.sort(key=lambda x: x[1])
    # print(positions)
    return ''.join([c[0] for c in positions])


def fix_numbers_with_letters_bad(line: str) -> str:
    digits = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8','nine': '9'}
    special_digits = {'oneight': '18', 'threeight': '38', 'fiveight': '58', 'nineight': '98', 'twone': '21', 'sevenine': '79', 'eightwo': '82', 'twoneight': '218',
                      'twoneighthree': '2183'}
    for d in special_digits:
        line = line.replace(d, special_digits[d])
    for d in digits:
        line = remplacer_occurrences(d, digits[d], line)
    return line

def fix_numbers_with_letters(line: str) -> str:
    digits = {'one': 'o1e', 'two': 't2o', 'three': 't3e', 'four': 'f4r', 'five': 'f5e', 'six': 's6x', 'seven': 's7n', 'eight': 'e8t','nine': 'n9e'}
    for d in digits:
        line = line.replace(d, digits[d])
    return line

with open('input.txt', 'r') as file:
    data = file.readlines()
    result: int = 0
    for input in data:
        line = input.strip()
        # print(line)
        line = list(fix_numbers_with_letters(line))
        line = list(filter(lambda x: x.isdigit(), line))
        # print(line)
        if len(line) > 1:
            tmp_result = int(line[0] + line[-1])
            # print(tmp_result)
        else:
            tmp_result = int(line[0]) * 2
        result += tmp_result
print(result)
