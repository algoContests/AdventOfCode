import re
from functools import reduce
from math import lcm, gcd
from typing import List

import sys


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()

def est_premier(nombre):
    if nombre < 2:
        return False
    for i in range(2, int(nombre**0.5) + 1):
        if nombre % i == 0:
            return False
    return True

def diviseurs(nombre):
    div = []
    for i in range(1, int(nombre**0.5) + 1):
        if nombre % i == 0:
            div.append(i)
            div.append(nombre // i)
    return div

def multiples(nombre):
    mult = []
    for i in range(1, int(nombre**0.5) + 1):
        if nombre % i == 0:
            mult.append(i)
            mult.append(nombre // i)
    return mult

def diviseurs2(nombre):
    diviseurs = []
    for i in range(1, nombre // 2 + 1):
        if nombre % i == 0:
            diviseurs.append(i)
    return diviseurs

def lcm2(a, b):
    return a * b // gcd(a, b)

def lcm3(*args):
    return reduce(lcm2, args)

if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()

    directions = data.split("\n")[0]
    nodes = {}

    current = []

    for node in data.split("\n\n")[1].split("\n"):
        src, left, right = re.findall(r"([A-Z]{3})", node)
        nodes[src] = (left, right)

        if src[2] == "A":
            current.append(src)

    debug(f'{len(directions)} directions: {directions}')
    debug(nodes)
    debug(current)

    # Algorithm

    steps: List[int] = []
    for c in current:
        node = c
        t = 0
        idx = 0
        while node[-1] != 'Z':
            move = directions[idx]
            idx = (idx + 1) % len(directions)
            node = nodes[node][0 if move == 'L' else 1]
            t += 1
        steps.append(t)

    print(len(directions), est_premier(len(directions)))
    print([(s, est_premier(s), diviseurs(s)) for s in steps])
    print([(s, est_premier(s), diviseurs2(s)) for s in steps])
    print([(s, est_premier(s), multiples(s)) for s in steps])
    print(reduce(lambda x, y: x * y, steps))
    print(lcm(*steps))
    print(lcm3(*steps))
    # 965799814374349812