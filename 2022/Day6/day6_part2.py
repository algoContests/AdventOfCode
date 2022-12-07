import os
from typing import List, Tuple

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        line: str = file.readline().replace('\n', '')
        mark: str = line[0]
        pos: int = 1
        while True:
            char: str = line[pos]
            if char in mark:
                duplicate_pos: List[int] = [i for i, c in enumerate(line) if c == char and i < pos]
                print(f'current (pos, char): ({pos, char}) - duplicate found -> {char} at position {duplicate_pos[-1]} after {len(mark)} different chars')
                pos = duplicate_pos[-1] + 1
                print(f'restart at: ({pos, line[pos]}) ')
                mark = line[pos]
            elif len(mark) < 13:
                mark += char
                print(mark)
            elif len(mark) == 13:
                mark += char
                break
            pos += 1

        print(pos + 1)