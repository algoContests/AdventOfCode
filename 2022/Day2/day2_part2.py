import os
from typing import List, Tuple

""" 
    A, X = ROCK
    B, Y = PAPER
    C, Z = SCISSORS
"""
if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    elves_food: List[int] = []
    loss: List[Tuple[str, str]] = dict([('A', 'Z'), ('B', 'X'), ('C', 'Y')])
    wins: List[Tuple[str, str]] = dict([('A', 'Y'), ('B', 'Z'), ('C', 'X')])
    draws: List[Tuple[str, str]] = dict([('A', 'X'), ('B', 'Y'), ('C', 'Z')])
    # strategy_table: dict = {'X': 0, 'Y': 3, 'Z': 6}
    scores: dict = {'X': 1, 'Y': 2, 'Z': 3}
    with open(file_name) as file:
        score: int = 0
        for line in file:
            a, b = map(str, line.split())
            if b == 'X':
                new_b = loss[a]
                score += scores[new_b]
            elif b == 'Y':
                new_b = draws[a]
                score += 3 + scores[new_b]
            else:
                new_b = wins[a]
                score += 6 + scores[new_b]

    print(score)


