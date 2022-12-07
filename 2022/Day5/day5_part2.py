import os
from typing import List, Tuple

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        stacks: List[List[str]] = [[] for _ in range(9)]
        crane_commands: List[Tuple[int, int, int]] = []
        for line in file:
            if 'move' in line:
                command: List[str] = line.replace('\n', '').split(' ')
                crates_count, start, end = int(command[1]), int(command[3]) - 1, int(command[5]) - 1
                crane_commands.append((crates_count, start, end))
            elif '[' in line:
                line = line.replace('\n', '').ljust(36, ' ')
                crates: List[str] = [line[4 * i + 1] for i in range(9)]
                for i, crate in enumerate(crates):
                    stacks[i].append(crate)

        for i in range(9):
            stacks[i].reverse()

        for stack in stacks:
            i = len(stack) - 1
            while i > 0 and stack[i] == ' ':
                stack.pop()
                i -= 1

        for crates_count, start, end in crane_commands:
            from_stack, to_stack = stacks[start], stacks[end]
            to_stack += from_stack[-crates_count:]
            stacks[start] = from_stack[:-crates_count]
            # from_stack = from_stack[:-crates_count]


        result = ''.join([s[-1] for s in stacks])

        print(result)
