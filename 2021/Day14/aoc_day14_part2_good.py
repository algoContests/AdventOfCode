""" --- Day 14: Extended Polymerization ---
https://adventofcode.com/2021/day/14#part2
https://culturesciences.chimie.ens.fr/thematiques/chimie-des-materiaux/polymeres/materiaux-polymeres-architecture-macromoleculaire
"""
import time

""" philRG tu n'es pas obligé de faire effectivement les insertions proposées, tu peux juste faire un "bilan" des lettres et des paires présentes
"""

STEPS_COUNT = 20


def count_insertions(p1, p2, step=1):
    global count_mol
    if step > STEPS_COUNT:
        return
    insert_mol = pairs[p1 + p2]
    count_mol[insert_mol] += 1
    count_insertions(p1, insert_mol, step + 1)
    count_insertions(insert_mol, p2, step + 1)


tic = time.time()

polymer = list(input())

polymer_str = ''.join(polymer)
print(f'polymer template = {polymer_str}')

blank_line = input()

pairs = {}
while True:
    try:
        pair, insert = input().split(' -> ')
        a, b = list(pair)
        pairs[a+b] = insert
    except EOFError:
        break

molecules = set(polymer)
count_mol = {mol: 0 for mol in sorted(molecules)} | {'S': 0}
for mol in polymer:
    count_mol[mol] += 1

print(count_mol)
for i in range(len(polymer) - 1):
    p1, p2 = polymer[i], polymer[i + 1]
    count_insertions(p1, p2)
    # least_common_mol = min(count_mol.items(), key=lambda x: x[1])
    # most_common_mol = max(count_mol.items(), key=lambda x: x[1])
    # print(f'step {i + 1} -> least_common_mol = {least_common_mol[0]}[{least_common_mol[1]}] - most_common_mol = {most_common_mol[0]}[{most_common_mol[1]}]')

least_common_mol = min(count_mol.items(), key=lambda x: x[1])
most_common_mol = max(count_mol.items(), key=lambda x: x[1])

print(f'least_common_mol = {least_common_mol[0]}[{least_common_mol[1]}] - most_common_mol = {most_common_mol[0]}[{most_common_mol[1]}]')

result = most_common_mol[1] - least_common_mol[1]

elapsed_time = time.time() - tic
seconds = round(elapsed_time, 3)

print(f'result = {result} for {STEPS_COUNT} steps in {seconds} seconds')

