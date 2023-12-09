import os
from typing import List

from numpy import array

TRAILING_MOVE = {
    (0, 0): (0, 0),

   (1, 0): (0, 0),
   (2, 0): (1, 0),
   (-1, 0): (0, 0),
   (-2, 0): (-1, 0),

   (0, 1): (0, 0),
   (0, 2): (0, 1),
   (0, -1): (0, 0),
   (0, -2): (0, -1),

   (1, 1): (0, 0),
   (-1, 1): (0, 0),
   (1, -1): (0, 0),
   (-1, -1): (0, 0),

   (2, 1): (1, 1),
   (-2, 1): (-1, 1),
   (2, -1): (1, -1),
   (-2, -1): (-1, -1),

   (1, 2): (1, 1),
   (-1, 2): (-1, 1),
   (1, -2): (1, -1),
   (-1, -2): (-1, -1),

   (2, 2): (1, 1),
   (-2, 2): (-1, 1),
   (2, -2): (1, -1),
   (-2, -2): (-1, -1)
}

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        directions = []
        for line in file:
            _dir, step = line.split()
            directions.append((_dir, int(step)))

    headPos, tailPos = array([0, 0]), array([0, 0])
    tailMarks: set() = {tuple(tailPos)}
    for _dir, step in directions:
        if _dir == 'R':
            for i in range(step):
                headPos[0] += 1
                diffPos: array = headPos - tailPos
                tailPos += array(TRAILING_MOVE[tuple(diffPos)])
                tailMarks.add(tuple(tailPos))
        elif _dir == 'L':
            for i in range(step):
                headPos[0] -= 1
                diffPos: array = headPos - tailPos
                tailPos += array(TRAILING_MOVE[tuple(diffPos)])
                tailMarks.add(tuple(tailPos))
        elif _dir == 'D':
            for i in range(step):
                headPos[1] += 1
                diffPos: array = headPos - tailPos
                tailPos += array(TRAILING_MOVE[tuple(diffPos)])
                tailMarks.add(tuple(tailPos))
        elif _dir == 'U':
            for i in range(step):
                headPos[1] -= 1
                diffPos: array = headPos - tailPos
                tailPos += array(TRAILING_MOVE[tuple(diffPos)])
                tailMarks.add(tuple(tailPos))

    result_part1 = len(tailMarks)
    print(f' Part 1 = {result_part1}')

    """ Part 2 """

    snake: List[array] = [array([0, 0]) for _ in range(10)]
    tailMarks: set() = {tuple(snake[9])}
    for _dir, step in directions:
        # print(snake)
        if _dir == 'R':
            for i in range(step):
                # print(snake[0])
                snake[0][0] += 1
                for j in range(1, 10):
                    diff: tuple = tuple(snake[j - 1] - snake[j])
                    # print(_dir, diff)
                    snake[j] += array(TRAILING_MOVE[diff])
                tailMarks.add(tuple(snake[9]))
        elif _dir == 'L':
            for i in range(step):
                # print(snake[0])
                snake[0][0] -= 1
                for j in range(1, 10):
                    diff: tuple = tuple(snake[j - 1] - snake[j])
                    # print(_dir, diff)
                    snake[j] += array(TRAILING_MOVE[diff])
                tailMarks.add(tuple(snake[9]))
        elif _dir == 'D':
            for i in range(step):
                # print(snake[0])
                snake[0][1] += 1
                for j in range(1, 10):
                    diff: tuple = tuple(snake[j - 1] - snake[j])
                    # print(_dir, diff)
                    snake[j] += array(TRAILING_MOVE[diff])
                tailMarks.add(tuple(snake[9]))
        elif _dir == 'U':
            for i in range(step):
                # print(snake[0])
                snake[0][1] -= 1
                for j in range(1, 10):
                    diff: tuple = tuple(snake[j - 1] - snake[j])
                    # print(_dir, diff)
                    snake[j] += array(TRAILING_MOVE[diff])
                tailMarks.add(tuple(snake[9]))

    result_part2 = len(tailMarks)
    print(f' Part 2 = {result_part2}')