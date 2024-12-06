""" --- Day 13: Transparent Origami --- """

def debug(paper: dict()):
    for y in range(max_y + 1):
        line = [paper[(x, y)] for x in range(max_x + 1)]
        line = ' '.join(list(map(str, line)))
        print(line)

dots = []
while True:
    try:
        x, y = map(int, input().split(','))
        dots.append((x, y))
    except ValueError:
        break

max_x = max(dots, key=lambda d: d[0])[0]
max_y = max(dots, key=lambda d: d[1])[1]

paper = {}
for y in range(max_y + 1):
    for x in range(max_x + 1):
        paper[(x, y)] = '#' if (x, y) in dots else '.'

fold_instructions = []
while True:
    try:
        m1, m2, m3 = input().split(' ')
        axis, value = m3.split('=')
        fold_instructions.append((axis, int(value)))
    except EOFError:
        break

# debug(paper)

print(f'max_x = {max_x} - max_y = {max_y}')
print(dots)
print(fold_instructions)

while fold_instructions:
    axis, value = fold_instructions.pop(0)
    if axis == 'x':
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if x > value and paper[(x, y)] == '#':
                    paper[(2 * value - x, y)] = '#'
        max_x = value - 1
    elif axis == 'y':
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                if y > value and paper[(x, y)] == '#':
                    paper[(x, 2 * value - y)] = '#'
        max_y = value - 1

print(f'max_x = {max_x} - max_y = {max_y}')
paper = dict([((x, y), dots) for (x, y), dots in paper.items() if x <= max_x and y <= max_y])

debug(paper)
# HZLEHJRK
