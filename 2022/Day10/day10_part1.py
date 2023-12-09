import os
from collections import namedtuple
from time import perf_counter
from typing import List

Statement = namedtuple('Statement', ['name', 'register'])

if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        statements = []
        for line in file:
            if len(line.split()) == 2:
                register = int(line.split()[1])
                statements.append(Statement('addx', register))
            else:
                statements.append(Statement('noop', 0))
    """
        Start by figuring out the signal being sent by the CPU. The CPU has a single register, X, which starts with the value 1. 
        It supports only two instructions:
            - addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be negative.)
            - noop takes one cycle to complete. It has no other effect.
        signal strength (the cycle number multiplied by the value of the X register)
    """

    start = perf_counter()

    X = 1
    cpu_cycle = 0
    signal_strength: List[int] = []
    registers = []
    for s in statements:
        if s.name == 'noop':
            cpu_cycle += 1
            signal_strength.append(cpu_cycle * X)
            registers.append(X)
        else:
            cpu_cycle += 1
            signal_strength.append(cpu_cycle * X)
            registers.append(X)
            cpu_cycle += 1
            signal_strength.append(cpu_cycle * X)
            registers.append(X)
            X += s.register

    cpu_cycle += 1
    signal_strength.append(cpu_cycle * X)
    registers.append(X)

""" 
    The sum of these signal strengths is 13140.
    Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles. What is the sum of these six signal strengths?
"""

result = sum([signal_strength[i-1] for i in range(20, 221, 40)])

print(result)
