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
    loss: List[Tuple[str, str]] = [('A', 'Z'), ('B', 'X'), ('C', 'Y')]
    wins: List[Tuple[str, str]] = [('A', 'Y'), ('B', 'Z'), ('C', 'X')]
    scores: dict = {'X': 1, 'Y': 2, 'Z': 3}
    with open(file_name) as file:
        score: int = 0
        for line in file:
            a, b = map(str, line.split())
            score += scores[b]
            score += 6 if (a, b) in wins else 0 if (a, b) in loss else 3

    print(score)


