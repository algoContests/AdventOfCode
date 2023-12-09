import re
from functools import reduce
from typing import List


def is_record(push_time: int, time: int, distance: int) -> bool:
    left_time, speed = time - push_time, push_time
    return speed * left_time > distance

with open('input.txt') as f:
    lines = f.read().split("\n")

time = list(map(int, lines[0].split(':')[1].split()))
# time2 = list(map(int, re.findall(r'(\d+)', lines[0])))
distance = list(map(int, lines[1].split(':')[1].split()))

map = [(time[i], distance[i]) for i in range(len(time))]
wins: dict = {}
for time, dist in map:
    wins[(time, dist)] = 0
    for push_time in range(time):
        if is_record(push_time, time, dist):
            wins[(time, dist)] += 1
result = reduce(lambda x, y: x * y, wins.values())
print(result)


