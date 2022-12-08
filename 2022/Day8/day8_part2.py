import os
from time import perf_counter


def scenic_score(x0, y0):
    tree_height = g[y0][x0]

    x, y = x0, y0
    viewing_distance_top = 0
    while y > 0:
        viewing_distance_top += 1
        y -= 1
        if g[y][x] >= tree_height:
            break

    x, y = x0, y0
    viewing_distance_bottom = 0
    while y < height - 1:
        viewing_distance_bottom += 1
        y += 1
        if g[y][x] >= tree_height:
            break

    x, y = x0, y0
    viewing_distance_left = 0
    while x > 0:
        viewing_distance_left += 1
        x -= 1
        if g[y][x] >= tree_height:
            break

    x, y = x0, y0
    viewing_distance_right = 0
    while x < width - 1:
        viewing_distance_right += 1
        x += 1
        if g[y][x] >= tree_height:
            break

    return viewing_distance_top * viewing_distance_bottom * viewing_distance_left * viewing_distance_right


if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        g = []
        for line in file:
            g.append(list(map(int, list(line.replace('\n', '')))))
        width, height = len(line), len(g)

    # print(g)

    # t = (2, 1)
    # print(f'{t} - scenic score = {scenic_score(*t)}')
    #
    # t = (2, 3)
    # print(f'{t} - scenic score = {scenic_score(*t)}')

    start = perf_counter()

    trees = [(x, y) for x in range(width) for y in range(height)]
    best_tree = max(trees, key=lambda t: scenic_score(*t))
    best_scenic_score = scenic_score(*best_tree)

    elapsed_time = (perf_counter() - start) * 1000
    print(f'best_tree = {best_tree} - scenic_score = {best_scenic_score} - elapsed time = {round(elapsed_time, 2)} ms')
