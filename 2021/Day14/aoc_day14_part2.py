""" --- Day 14: Extended Polymerization ---
https://adventofcode.com/2021/day/14#part2
https://culturesciences.chimie.ens.fr/thematiques/chimie-des-materiaux/polymeres/materiaux-polymeres-architecture-macromoleculaire
"""
import time
from collections import deque
from multiprocessing import Pool

""" philRG tu n'es pas obligé de faire effectivement les insertions proposées, tu peux juste faire un "bilan" des lettres et des paires présentes
"""

STEPS_COUNT = 20

def count_insertions(p1, p2, step=1):
    queue = deque([(p1, p2, step)])
    count_mol = {mol: 0 for mol in sorted(molecules)} | {'S': 0}
    while queue:
        p1, p2, step = queue.pop()
        if step > STEPS_COUNT:
            continue
        insert_mol = pairs[p1 + p2]
        count_mol[insert_mol] += 1
        queue.append((p1, insert_mol, step + 1))
        queue.append((insert_mol, p2, step + 1))
    return count_mol


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
init_count = {mol: 0 for mol in sorted(molecules)} | {'S': 0}
for mol in polymer:
    init_count[mol] += 1

count_mol_list = []
for i in range(len(polymer) - 1):
    p1, p2 = polymer[i], polymer[i + 1]
    count_mol_list.append(count_insertions(p1, p2))

count_mol = init_count
for c_mol in count_mol_list:
    for key, value in c_mol.items():
        count_mol[key] += c_mol[key]

least_common_mol = min(count_mol.items(), key=lambda x: x[1])
most_common_mol = max(count_mol.items(), key=lambda x: x[1])

print(f'least_common_mol = {least_common_mol[0]}[{least_common_mol[1]}] - most_common_mol = {most_common_mol[0]}[{most_common_mol[1]}]')

result = most_common_mol[1] - least_common_mol[1]

elapsed_time = time.time() - tic
seconds = round(elapsed_time, 3)

print(f'result = {result} for {STEPS_COUNT} steps in {seconds} seconds')



