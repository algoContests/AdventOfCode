""" --- Day 15: Chiton ---"""
import heapq

import math
from collections import deque

import numpy as np


def bfs():
    """ Y a pas bon le bfs philRG ici """
    queue = deque([(0, [(0, 0)])])
    min_risk = math.inf
    best_path = []
    visited = [(0, 0)]
    while queue:
        risk, path = queue.popleft()
        x, y = path[-1]
        if (x, y) == (9, 9) and risk < min_risk:
            best_path = path
            min_risk = risk
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            n_x, n_y = x + dx, y + dy
            if not in_grid(n_x, n_y) or (n_x, n_y) in path:
                continue
            queue.append((risk + chitons[n_x, n_y], path + [(n_x, n_y)]))
            # visited.append((n_x, n_y))
    return best_path, min_risk


def dijkstra():
    """ tentative d'implémenter le pseudo-code de pardouin """
    start, end = (0, 0), (99, 99)
    pqueue = [(0, start)]
    dist_dans_pqueue = {start: 0}
    deja_fait = set()

    while pqueue:
        dist, sommet = heapq.heappop(pqueue)
        if sommet in deja_fait:
            continue
        deja_fait.add(sommet)
        x, y = sommet
        voisins = []
        for s in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
            if in_grid(*s):
                d = dist_dans_pqueue[s] if s in dist_dans_pqueue else chitons[x, y]
                voisins.append((s, d))
        for s, d in voisins:
            nouv_d = dist + d
            if s in deja_fait:
                continue
            if s == end:
                return nouv_d
            if s not in dist_dans_pqueue or dist_dans_pqueue[s] > nouv_d:
                heapq.heappush(pqueue, (nouv_d, s))
                dist_dans_pqueue[s] = nouv_d


chitons = np.zeros(shape=(100, 100), dtype=int)
y = 0
while True:
    try:
        for x, value in enumerate(map(int, input())):
            chitons[x, y] = value
        y += 1
    except EOFError:
        break

in_grid = lambda x, y: 0 <= x < 100 and 0 <= y < 100

# chitons.transpose()

risk = dijkstra()

print(f'risk = {risk}')
