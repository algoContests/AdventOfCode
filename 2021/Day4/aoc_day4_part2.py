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
            # debug(f'win on col #{y}')
            return True
    # Check cols
    for x in range(5):
        marks = 0
        for y in range(5):
            if grid[(x, y)][1]:
                marks += 1
        if marks == 5:
            # debug(f'win on col #{x}')
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

"""     
    Stratégie : il faut juste penser à dégager les grilles gagnantes du pool au fur et à mesure
"""
# bingo_flag = False
# for bingo_number in bingo_numbers:
#     # if bingo_flag:
#     #     print(f'bingo number: {last_bingo_number} \n {formatted(winning_grid)} \n result = {result}')
#     #     break
#     i = 0
#     while bingo_grids and i < len(bingo_grids):
#         grid = bingo_grids[i]
#         # for grid in bingo_grids:
#         for (x, y), (number, mark) in grid.items():
#             if number == bingo_number:
#                 grid[(x, y)] = (number, True)
#         if check_win(grid):
#             # print(f'grid #{bingo_grids.index(grid)} wins with bingo number = {bingo_number}!')
#             # print(f'bingo: {bingo_number} \n {formatted(grid)}')
#             somme = sum([number for (x, y), (number, mark) in grid.items() if not mark])
#             result = somme * bingo_number
#             last_bingo_number, winning_grid = bingo_number, grid
#             bingo_flag = True
#             last_grid = grid
#             bingo_grids.remove(grid)
#         i += 1

loser = False

for number in bingo_numbers:
    i = 0
    for grid in bingo_grids:
        #grid.checkNumber(number)
        if check_win(grid):
            lastWinner = bingo_grids.pop(i)
            last_bingo_number = number
        if len(bingo_grids) < 1:
            loser = True
            break
        # Next Board
        i += 1
    if loser:
        break

somme = sum([number for (x, y), (number, mark) in lastWinner.items() if not mark])
result = somme * last_bingo_number
print(f'bingo: {last_bingo_number} - result = {result} \n {formatted(lastWinner)}')

# print(f'bingo: {last_bingo_number} \n {formatted(winning_grid)}')
# print(f'grid #{bingo_grids.index(winning_grid)} wins with bingo number = {last_bingo_number}!')
#
# # print(f'bingo: {bingo_number} \n {formatted(random_grid)}')
#
# print(result)


