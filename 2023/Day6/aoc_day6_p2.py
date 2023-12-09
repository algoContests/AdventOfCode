import re
from functools import reduce
from typing import List


def is_record(push_time: int, time: int, distance: int) -> bool:
    left_time, speed = time - push_time, push_time
    return speed * left_time > distance

with open('input.txt') as f:
    lines = f.read().split("\n")

time = int(''.join(lines[0].split(':')[1].split()))
dist = int(''.join(lines[1].split(':')[1].split()))

wins = [push_time for push_time in range(time) if is_record(push_time, time, dist)]
print(len(wins))