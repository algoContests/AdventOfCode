import os
from typing import List, Tuple

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        line: str = file.readline()
        mark: str = line[0]
        pos: int = 0
        while True:
            pos += 1
            char: str = line[pos]
            if char in mark:
                duplicate_pos: List[int] = [i for i, c in enumerate(line) if c == char and i < pos]
                pos = duplicate_pos[-1] + 1
                mark = line[pos]
            elif len(mark) < 4:
                mark += char
            elif len(mark) == 4:
                break

        print(pos)