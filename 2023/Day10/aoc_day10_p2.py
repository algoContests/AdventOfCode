import sys, re
from collections import deque

from typing import List
from matplotlib import pyplot as plt
import numpy as np


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()


def plot_polygon(polygon):
    """
    Affiche un polygone à l'aide de Matplotlib.
    :param polygon: Liste des sommets du polygone [(x1, y1), (x2, y2), ..., (xn, yn)]
    """
    polygon.append(polygon[0])  # Ajoute le premier sommet à la fin pour fermer le polygone

    x, y = zip(*polygon)  # Sépare les coordonnées x et y

    plt.plot(x, y, marker='o', linestyle='-')
    plt.fill(x, y, alpha=0.3)  # Remplit le polygone avec une transparence

    plt.xlabel('Coordonnée x')
    plt.ylabel('Coordonnée y')
    plt.title('Affichage d\'un polygone')
    plt.grid(True)
    # plt.gca().invert_xaxis()
    plt.xlim(0, max(x) + 1)
    plt.ylim(0, max(y) + 1)
    plt.gca().invert_yaxis()
    plt.show()


def is_point_inside_polygon_bad(x, y, polygon):
    """
    Vérifie si un point est dans un polygone.
    :param x: Abscisse du point
    :param y: Ordonnée du point
    :param polygon: Liste des sommets du polygone [(x1, y1), (x2, y2), ..., (xn, yn)]
    :return: True si le point est dans le polygone, False sinon
    """
    n = len(polygon)
    inside = False

    x1, y1 = polygon[0]
    for i in range(n + 1):
        x2, y2 = polygon[i % n]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                        # Si l'intersection est à gauche du point, on bascule l'état 'inside'
                        if xinters < x:
                            inside = not inside
    return inside

def is_point_inside_polygon(x, y, polygon):
    """
    Vérifie si un point est dans un polygone.
    :param x: Abscisse du point
    :param y: Ordonnée du point
    :param polygon: Liste des sommets du polygone [(x1, y1), (x2, y2), ..., (xn, yn)]
    :return: True si le point est dans le polygone, False sinon
    """
    n = len(polygon)
    inside = False

    x1, y1 = polygon[0]
    for i in range(n + 1):
        x2, y2 = polygon[i % n]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                        # Si l'intersection est à gauche du point, on bascule l'état 'inside'
                        if xinters < x:
                            inside = not inside
        x1, y1 = x2, y2  # Met à jour les coordonnées du sommet précédent
    return inside


# def point_inside_polygon(x, y, polygon):
#     """
#     Vérifie si un point (x, y) est à l'intérieur d'un polygone concave.
#     :param x: Coordonnée x du point
#     :param y: Coordonnée y du point
#     :param polygon: Liste des sommets du polygone [(x1, y1), (x2, y2), ..., (xn, yn)]
#     :return: True si le point est à l'intérieur, False sinon
#     """
#     n = len(polygon)
#     inside = False
#
#     for i in range(n):
#         x1, y1 = polygon[i]
#         x2, y2 = polygon[(i + 1) % n]
#
#         # Test d'intersection avec le rayon horizontal partant du point vers l'extérieur
#         if ((y1 <= y < y2) or (y2 <= y < y1)) and (x < max(x1, x2)):
#             # Calcul de l'intersection du rayon avec le segment
#             x_intersect = (y - y1) * (x2 - x1) / (y2 - y1) + x1
#
#             # Si l'intersection est à gauche du point, on bascule l'état 'inside'
#             if x_intersect < x:
#                 inside = not inside
#
#     return inside

def is_point_inside_polygon(x, y, polygon):
    """
    Vérifie si un point est dans un polygone.
    :param x: Abscisse du point
    :param y: Ordonnée du point
    :param polygon: Liste des sommets du polygone [(x1, y1), (x2, y2), ..., (xn, yn)]
    :return: True si le point est dans le polygone, False sinon
    """
    n = len(polygon)
    inside = False

    x1, y1 = polygon[0]
    for i in range(n + 1):
        x2, y2 = polygon[i % n]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                        # Si l'intersection est à gauche du point, on bascule l'état 'inside'
                        if x1 == x2 or x <= xinters:
                            inside = not inside
        x1, y1 = x2, y2  # Met à jour les coordonnées du sommet précédent
    return inside


# ymax=max{ yi; 1≤i≤n }
# R=(x;ymax+1)
# cpt=0
# Pour i de 1 à n
#   Si xi≠xi+1
#     m=(yi+1-yi)/(xi+1-xi)
#     p=yi-m*xi
#     xI=x
#     yI=m*x+p
#   Fin
#   Si ((xI-xi)*(xI-xi+1})<0 & (yI-yR)*(y-yI)<0)
#     cpt=cpt+1
#   Fin
#  Si (cpt est pair): M est à l'intérieur
#  Sinon: M est à l'extérieur

def inside_polygon(x, y, polygon):
    y_max = max(yi for xi, yi in polygon)
    R = (x, y_max + 1)
    yR = y_max + 1
    cpt = 0
    for i in range(len(polygon) - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
            p = y1 - m * x1
            xI = x
            yI = m * x + p
        # else:
        #     xI = x1
        #     yI = y1
        if ((xI - x1) * (xI - x2)) < 0 and (yI - y1) * (y - yI) < 0:
            cpt += 1
    return cpt % 2 == 0

if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()
        lines = data.splitlines()
        grid = []
        for line in lines:
            if 'S' in line:
                start = (line.index('S'), lines.index(line))
                line = line.replace('S', 'a')
            grid.append(list(line))

        # print(lines)
        # for line in grid:
        #     print(line)

        """
            | is a vertical pipe connecting north and south.
            - is a horizontal pipe connecting east and west.
            L is a 90-degree bend connecting north and east.
            J is a 90-degree bend connecting north and west.
            7 is a 90-degree bend connecting south and west.
            F is a 90-degree bend connecting south and east.
        """
        coming_from_dir = {'W': ('-', 'J', '7'), 'N': ('|', 'L', 'J'), 'E': ('-', 'L', 'F'), 'S': ('|', '7', 'F')}
        possible_dirs = {'a': ('E', 'S', 'N', 'W'), 'F': ('E', 'S'), '|': ('N', 'S'), '-': ('W', 'E'), 'L': ('N', 'E'),
                         'J': ('N', 'W'), '7': ('S', 'W')}
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # 'Coming from': ['W', 'N', 'E', 'S']
        dirs = {'E': (1, 0), 'S': (0, 1), 'W': (-1, 0), 'N': (0, -1)}
        geos = ['E', 'S', 'W', 'N']
        reverse_geos = ['W', 'N', 'E', 'S']
        w, h = len(grid[0]), len(grid)

        """
            .....
            .S-7.
            .|.|.
            .L-J.
            .....
        """


        def get_moves(pos):
            x, y = pos
            moves = []
            for _dir, (dx, dy) in dirs.items():
                from_cell_value = grid[y][x]
                if _dir not in possible_dirs[from_cell_value]:
                    continue
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= w or ny < 0 or ny >= h:
                    continue
                to_cell_value = grid[ny][nx]
                if to_cell_value == '.':
                    continue
                opposite_dir = reverse_geos[geos.index(_dir)]
                if opposite_dir not in possible_dirs[to_cell_value]:
                    continue
                moves.append((nx, ny))
            return moves


        moves = get_moves(start)
        polygon = [start]
        next = moves[0]
        visited = {start, next}
        while True:
            # debug(next)
            moves = [m for m in get_moves(next) if m not in visited]
            if not moves:
                #polygon.append(start)
                break
            next = moves[0]
            polygon.append(next)
            visited.add(next)

        print(f'polygone à {len(polygon)} sommets')
        # print(polygon)

        points_inside_polygon = [(x, y) for x in range(w) for y in range(h) if is_point_inside_polygon(x, y, polygon) and (x, y) not in polygon]

        invert = lambda p: (p[0], h - p[1])
        #print(list(map(invert, points_inside_polygon)))
        print(points_inside_polygon)
        # plot_polygon(polygon)
        print(len(points_inside_polygon) - 1)   # 416 ou 417?

        # # Exemple d'utilisation
        # polygon_example = [(1, 1), (2, 3), (4, 5), (5, 2), (3, 1)]
        #
        #
        # points_inside_polygon = [(x, y) for x in range(w) for y in range(h) if
        #                          is_point_inside_polygon(x, y, polygon_example) and (x, y) not in polygon_example]
        #
        # print(points_inside_polygon)
        # plot_polygon(polygon_example)