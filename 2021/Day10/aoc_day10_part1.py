from collections import deque
from typing import List

score = 0


def check_line(line: str):
    carets = {'[': ']', '(': ')', '{': '}', '<': '>'}
    queue: List = list(line)
    print(f'processing line : {line}')
    while queue:
        print(f'queue length : {len(queue)} - new queue: {"".join(queue)}')
        # if len(queue) == 8:
        #     exit(0)
        closing_carets = [c for c in queue if c in carets.values()]
        if not closing_carets:
            return False
        for i, caret in enumerate(queue):
            if caret in carets.values():
                prev_caret = queue[i - 1]
                if caret == carets[prev_caret]:
                    print(f'deleting chunk position ({i - 1}, {i}) : {prev_caret}{caret}')
                    queue.pop(i - 1)
                    queue.pop(i - 1)
                    print(f'queue length : {len(queue)} - new queue: {"".join(queue)}')
                    break
                else:
                    return False
    return True


i = 0
legal_count = 0
illegal_count = 0
while True:
    try:
        line = input()
        if not check_line(line):
            illegal_count += 1
            # print(f'illegal line #{i}: {line}')
        else:
            legal_count += 1
            # print(f'legal line #{i}: {line}')
        i += 1
    except EOFError:
        print(f'{legal_count} legal line')
        print(f'{illegal_count} illegal line')
        break
