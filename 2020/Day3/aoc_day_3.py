rows, cols = 323, 31

x, y = (0, 0)
trees_count = 0
forest = []
for _ in range(rows):
    line = input()
    tab = list(line)
    while x > len(tab):
        tab += tab
    forest.append(tab)
    if tab[x] == '#':
        trees_count += 1
    x += 3

print(trees_count)
