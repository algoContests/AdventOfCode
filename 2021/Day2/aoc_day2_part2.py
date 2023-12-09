import math
from typing import Tuple, List, Optional
import sys
print(sys.getdefaultencoding())

# 👾 = 2
𝞟 = 3.14
"""--- Part Two ---
    Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.
    
    In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:
    
    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        It increases your horizontal position by X units.
        It increases your depth by your aim multiplied by X.
"""

# pas recommandé, mais autorisé par le langage
nb_élèves = 12

print(nb_élèves)

DIRECTIONS = {'forward': (1, 0), 'up': (0, -1), 'down': (0, 1)}
x, y, aim = 0, 0, 0
while True:
    try:
        direction, move = input().split()
        move = int(move)
        if direction == 'forward':
            dx, dy = DIRECTIONS[direction]
            x += move * dx
            y += move * aim
        else:
            aim = aim - move if direction == 'up' else aim + move
    except EOFError:
        # print(x, y)
        print(x * y)
        break
