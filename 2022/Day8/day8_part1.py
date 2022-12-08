import os
from time import perf_counter


def get_visible_trees(grid):
    visible_trees = []
    # FROM TOP
    for x in range(1, width - 1):
        biggest = g[0][x]
        for y in range(1, height - 1):
            if g[y][x] > biggest:
                biggest = g[y][x]
                visible_trees.append((x, y))
    # FROM BOTTOM
    for x in range(1, width - 1):
        biggest = g[height - 1][x]
        for y in range(height - 2, 0, -1):
            if g[y][x] > biggest:
                biggest = g[y][x]
                visible_trees.append((x, y))
    # FROM LEFT
    for y in range(1, height - 1):
        biggest = g[y][0]
        for x in range(1, width - 1):
            if g[y][x] > biggest:
                biggest = g[y][x]
                visible_trees.append((x, y))
    # FROM RIGHT
    for y in range(1, height - 1):
        biggest = g[y][width - 1]
        for x in range(width - 2, 0, -1):
            if g[y][x] > biggest:
                biggest = g[y][x]
                visible_trees.append((x, y))

    return visible_trees

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        g = []
        for line in file:
            g.append(list(line.replace('\n', '')))
        width, height = len(line), len(g)

    # print(g)

    start = perf_counter()

    visible_trees = get_visible_trees(g)

    tree_visible_from_interior = len(list(set(visible_trees)))
    tree_visible_from_edges = 2 * width + 2 * (height - 2)
    print(f'tree_visible_from_interior = {tree_visible_from_interior}')
    print(f'tree_visible_from_edges = {tree_visible_from_edges}')
    print(tree_visible_from_interior + tree_visible_from_edges)

    elapsed_time = (perf_counter() - start) * 1000
    print(f'elapsed time = {round(elapsed_time, 2)} ms')

