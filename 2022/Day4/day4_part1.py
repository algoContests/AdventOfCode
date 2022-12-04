import os
from typing import List

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        assignement_pairs = 0
        for line in file:
            range_1, range_2 = line.split(',')
            start_1, end_1 = map(int, range_1.split('-'))
            start_2, end_2 = map(int, range_2.split('-'))
            set_1 = set(range(start_1, end_1 + 1))
            set_2 = set(range(start_2, end_2 + 1))
            if set_1 <= set_2 or set_2 <= set_1:
                assignement_pairs += 1
                # print(range_1, range_2, end='')
        print(assignement_pairs)