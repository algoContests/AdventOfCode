import random
import sys
import re


def debug(*args):
    # return
    print(*args, file=sys.stderr, flush=True)


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def formatted(grid: dict()) -> str:
    formatted_grid = ""
    for y in range(5):
        for x in range(5):
            number, mark = grid[(x, y)]
            w_spaces = "  " if len(str(number)) == 1 else " "
            if mark:
                formatted_grid += w_spaces + color.GREEN + str(number) + color.END
            else:
                formatted_grid += w_spaces + str(number)
        formatted_grid += "\n"
        formatted_grid = formatted_grid.lstrip()
    return formatted_grid


def check_win(grid: dict()):
    # Check rows
    for y in range(5):
        marks = 0
        for x in range(5):
            if grid[(x, y)][1]:
                marks += 1
        if marks == 5:
            debug(f'win on col #{y}')
            return True
    # Check cols
    for x in range(5):
        marks = 0
        for y in range(5):
            if grid[(x, y)][1]:
                marks += 1
        if marks == 5:
            debug(f'win on col #{x}')
            return True
    # # Check first diagonal
    # marks = 0
    # for x in range(5):
    #     for y in range(5):
    #         if x == y and grid[(x, y)][1]:
    #             marks += 1
    # if marks == 5:
    #     debug('win on 1st diagonal')
    #     return True
    # # Check second diagonal
    # marks = 0
    # for x in range(4, -1, -1):
    #     for y in range(5):
    #         if x == y and grid[(x, y)][1]:
    #             marks += 1
    # if marks == 5:
    #     debug('win on 2nd diagonal')
    #     return True
    return False


bingo_numbers = list(map(int, input().split(',')))
boards = []
line = input()
line = input()
bingo_grids = []
grid = {}
x, y = 0, 0
while True:
    try:
        if line == '':
            bingo_grids.append(grid)
            grid = {}
            x, y = 0, 0
        else:
            line = re.sub("[ ]{2,}", " ", line).lstrip()
            numbers = list(map(int, line.split(' ')))
            for x, number in enumerate(numbers):
                grid[(x, y)] = (number, False)
            y += 1
        line = input()
    except ValueError:
        debug(f'input line = {line}')
    except EOFError:
        break

bingo_flag = False
for bingo_number in bingo_numbers:
    if bingo_flag:
        break
    for grid in bingo_grids:
        if bingo_flag:
            break
        for (x, y), (number, mark) in grid.items():
            if number == bingo_number:
                grid[(x, y)] = (number, True)
        if check_win(grid):
            print(f'grid #{bingo_grids.index(grid)} wins with bingo number = {bingo_number}!')
            print(f'bingo: {bingo_number} \n {formatted(grid)}')
            somme = sum([number for (x, y), (number, mark) in grid.items() if not mark])
            result = somme * bingo_number
            bingo_flag = True
            break


# random_grid = random.choice(bingo_grids)
# print(f'bingo: {bingo_number} \n {formatted(random_grid)}')

print(result)

