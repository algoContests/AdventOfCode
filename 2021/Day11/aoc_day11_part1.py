""" --- Day 11: Dumbo Octopus --- """
from typing import Tuple, List, Optional
import sys

sys.setrecursionlimit(15000)


def debug(octopus: dict()):
    for y in range(n):
        line = [octopus[(x, y)][0] for x in range(n)]
        line = ' '.join(list(map(str, line)))
        print(line)


def get_adjacent_octopus_positions(x, y):
    adjacent_octopus_positions = []
    for dx in range(-1, 2, 1):
        for dy in range(-1, 2, 1):
            if (dx, dy) != (0, 0):
                n_x, n_y = x + dx, y + dy
                if 0 <= n_x < n and 0 <= n_y < n:
                    adjacent_octopus_positions.append((n_x, n_y))
    return adjacent_octopus_positions


def flash_adjacent_octopus(x, y):
    global recurse_count, octopus, flashes
    recurse_count += 1
    adjacent_octopus_positions = get_adjacent_octopus_positions(x, y)
    for adj_pos in adjacent_octopus_positions:
        octopus[adj_pos][0] += 1
        if octopus[adj_pos][0] > 9 and octopus[adj_pos][1]:
            flashes += 1
            octopus[adj_pos][1] = False     # Octopus has flashed
            flash_adjacent_octopus(*adj_pos)


# in_grid = lambda x, y: 0 <= x < 10 and 0 <= y < 10
""" Read inputs """
n = 10
octopus = {}
for y in range(n):
    line = input()
    for x, energy in enumerate(line):
        can_flash = True
        octopus[(x, y)] = [int(energy), can_flash]

debug(octopus)

recurse_count = 0
flashes = 0
for step in range(100):
    """ First, the energy level of each octopus increases by 1.
    """
    for key, value in octopus.items():
        energy, can_flash = value
        octopus[key] = [energy + 1, True]

    """ Then, any octopus with an energy level greater than 9 flashes.
        This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. 
        If this causes an octopus to have an energy level greater than 9, it also flashes. 
        This process continues as long as new octopuses keep having their energy level increased beyond 9. 
        (An octopus can only flash at most once per step.)
    """
    try:
        flashing_octopus = [pos for pos, (energy, can_flash) in octopus.items() if energy > 9 and can_flash]
        while flashing_octopus:
            flashes += 1
            pos = flashing_octopus.pop(0)
            octopus[pos][1] = False     # Octopus has flashed
            flash_adjacent_octopus(*pos)
            flashing_octopus = [pos for pos, (energy, can_flash) in octopus.items() if energy > 9 and can_flash]
    except RecursionError:
        print(f'Recursion error - step {step} - recurse_count = {recurse_count}')

    """ Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash."""
    for key, value in octopus.starting_items():
        energy, can_flash = value
        if energy > 9 and not can_flash:
            octopus[key] = [0, can_flash]

    print(f'Step {step}')
    debug(octopus)

print(flashes)
