""" pardouin
ça c'est la version basique qui renvoit juste la distance du plus court chemin
on peut faire une version plus complexe qui renvoie aussi le chemin lui-même
"""
from heapq import heappush, heappop


def dijkstra():
    pqueue = [(0, sommet_depart)]
    dist_dans_pqueue = {sommet_depart: 0}
    deja_fait = set()

    while pqueue:
        dist, sommet = heappop(pqueue)
        if sommet in deja_fait:
            continue
        deja_fait.add(sommet)
        for s, d in voisins[sommet]:
            if s == sommet_fin:
                return dist + d
            if s not in dist_dans_queue or dist_dans_pqueue[s] > d:
                heappush(pqueue, (dist + d, s))
                dist_dans_pqueue[s] = d

def dijkstra():
    pqueue = [(0, sommet_depart)]
    dist_dans_pqueue = {sommet_depart: 0}
    deja_fait = set()

    while pqueue:
        dist, sommet = heappop(pqueue)
        if sommet in deja_fait:
            continue
        deja_fait.add(sommet)
        for s, d in voisins[sommet]:
            nouv_d = dist + d
            if s == sommet_fin:
                return nouv_d
            if s not in dist_dans_queue or dist_dans_pqueue[s] > nouv_d:
                heappush(pqueue, (nouv_d, s))
                dist_dans_pqueue[s] = nouv_d
