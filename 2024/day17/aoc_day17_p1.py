import re


def process_file(filename):
    with open(filename) as f:
        data = f.read()
    return ([int(x) for x in re.findall(r'Register \w: (\d+)', data)],
            [int(x) for x in re.search(r'Program: ([\d,]+)', data).group(1).split(',')])


def part_1(registers, program):
    # Initialize registers and instruction pointer
    A, B, C = registers
    ip = 0  # Instruction pointer
    output = []

    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        else:
            raise ValueError("Invalid combo operand")

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        ip += 2  # Default increment

        if opcode == 0:  # adv
            A //= 2 ** get_combo_value(operand)
        elif opcode == 1:  # bxl
            B ^= operand
        elif opcode == 2:  # bst
            B = get_combo_value(operand) % 8
        elif opcode == 3:  # jnz
            if A != 0:
                ip = operand
        elif opcode == 4:  # bxc
            B ^= C
        elif opcode == 5:  # out
            output.append(get_combo_value(operand) % 8)
        elif opcode == 6:  # bdv
            B = A // (2 ** get_combo_value(operand))
        elif opcode == 7:  # cdv
            C = A // (2 ** get_combo_value(operand))
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    return ','.join(map(str, output))


def part_2(registers, program):
    pass


def main() -> None:
    registers, program = process_file('input.txt')

    print(f"result aoc day 17 - p1: {part_1(registers, program)}")


if __name__ == "__main__":
    main()

