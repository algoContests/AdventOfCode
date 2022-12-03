import os

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        priority_sum = 0
        for line in file:
            cut: int = len(line) // 2
            left_c, right_c = set(line[:cut]), set(line[cut:])
            # print(left_c, right_c)
            errors: str = left_c.intersection(right_c)
            if errors:
                letter = errors.pop()
                offset = 65 - 27 if letter.isupper() else 96
                priority_sum += ord(letter) - offset
        print(priority_sum)
