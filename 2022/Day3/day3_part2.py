import os
from typing import List

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        g_three: List[str] = []
        priority_sum = 0
        line_count = 0
        for line in file:
            line_count += 1
            g_three.append(set(line))
            if not line_count % 3:
                count = 0
                common_badges = g_three[0].intersection(g_three[1]).intersection(g_three[2])
                if '\n' in common_badges:
                    common_badges.remove('\n')
                print(common_badges)
                g_three: List[str] = []
                if common_badges:
                    letter = common_badges.pop()
                    offset = 65 - 27 if letter.isupper() else 96
                    priority_sum += ord(letter) - offset
        print(priority_sum)
