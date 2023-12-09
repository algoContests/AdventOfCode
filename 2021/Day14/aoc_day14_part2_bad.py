""" --- Day 14: Extended Polymerization ---
https://adventofcode.com/2021/day/14#part2
https://culturesciences.chimie.ens.fr/thematiques/chimie-des-materiaux/polymeres/materiaux-polymeres-architecture-macromoleculaire
"""
""" philRG tu n'es pas obligé de faire effectivement les insertions proposées, tu peux juste faire un "bilan" des lettres et des paires présentes
"""
import time

STEPS_COUNT = 10

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
        pairs[(a, b)] = insert
    except EOFError:
        break

insert_mol = set(pairs.values())
new_molecules = [mol for mol in insert_mol if mol not in polymer]
new_molecules_str = ''.join(new_molecules)
print(f'{len(new_molecules)} new molecule(s) will be inserted = {new_molecules_str}')

molecules = set(polymer)
print(f'{len(molecules)} different molecules in template polymer : {sorted(molecules)}')

old_polymer = polymer
step = 0
new_polymer = []
for _ in range(40):
    step += 1
    for i in range(len(old_polymer) - 1):
        p1, p2 = old_polymer[i], old_polymer[i + 1]
        new_polymer = [p1, p2]
        for _ in range(STEPS_COUNT):
            new_polymer.append(p1)
            new_polymer.append(pairs[(p1, p2)])
    new_polymer.append(old_polymer[-1])
    old_polymer = new_polymer
    print(f'step {step} processed in {round((time.time() - tic) * 1000)}ms')
    # old_polymer_str, new_polymer_str = ''.join(polymer), ''.join(new_polymer)
    # print(f'step #{step} : old polymer = {old_polymer_str} - new polymer = {new_polymer_str}')

count_mol = {}
molecules = set(new_polymer)
print(f'{len(molecules)} different molecules in resulting polymer : {sorted(molecules)}')
print(f'resulting polymer length = {len(new_polymer)}')

new_polymer_str = ''.join(new_polymer)
for mol in molecules:
    count_mol[mol] = new_polymer_str.count(mol)

least_common_mol = min(count_mol.items(), key=lambda x: x[1])
most_common_mol = max(count_mol.items(), key=lambda x: x[1])

print(f'least_common_mol = {least_common_mol[0]}[{least_common_mol[1]}] - most_common_mol = {most_common_mol[0]}[{most_common_mol[1]}]')

result = most_common_mol[1] - least_common_mol[1]

print(f'result = {result} after {step} steps')

print(f'elapsed time = {round((time.time() - tic) * 1000)}ms')
