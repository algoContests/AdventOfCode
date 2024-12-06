import math
from typing import Tuple, List, Optional

""" --- Day 2: Dive! ---
    Now, you need to figure out how to pilot this thing.

    It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

    forward X increases the horizontal position by X units.
    down X increases the depth by X units.
    up X decreases the depth by X units.
"""

DIRECTIONS = {"forward": (1, 0), 'up': (0, -1), 'down': (0, 1)}
x, y = 0, 0
while True:
    try:
        direction, distance = input().split()
        dx, dy = DIRECTIONS[direction]
        x += int(distance) * dx
        y += int(distance) * dy
    except EOFError:
        print(x, y)
        print(x * y)
        break
