import os
from typing import List


if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    elves_food: List[int] = []
    food: int = 0
    with open(file_name) as file:
        for line in file:
            if line == '\n':
                elves_food.append(food)
                food = 0
                continue
            food += int(line)

    print(max(elves_food))
