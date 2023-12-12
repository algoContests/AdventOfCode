import re
from dataclasses import dataclass
from itertools import product
from typing import List

from tools import debug


@dataclass
class Instruction:
    records: List[str]
    counts: List[int]
    unknown: List[int] = None

    def __post_init__(self):
        self.unknown = [i for i, c in enumerate(self.records) if c == '?']

    @property
    def is_valid(self) -> bool:
        line = ''.join(self.records)
        groups: List[int] = re.findall(r'(#+)', line)
        return len(groups) == len(self.counts) and all(len(groups[i]) == c for i, c in enumerate(self.counts))

    def __copy__(self):
        return Instruction([*self.records], self.counts)

    def __repr__(self):
        return f'{self.records} groups: {self.counts} - unknown: {self.unknown}'


def generer_combinaisons_bool(n) -> List[tuple]:
    return list(product([True, False], repeat=n))


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().strip()
        lines = data.splitlines()

        #debug(lines)

    instructions: List[Instruction] = []
    for line in lines:
        records, counts = line.split()
        new_records = list(records)
        for _ in range(4):
            new_records += ['?'] + list(records)
        counts = list(map(int, counts.split(','))) * 5
        instructions.append(Instruction(new_records, counts))

    # debug(data)

    total: int = 0
    for instr in instructions:
        n: int = len(instr.unknown)
        arrangements: List[tuple] = generer_combinaisons_bool(n)
        print(f'generating {len(arrangements)} arrangements for {instr}')
        for arrangement in arrangements:
            instr_copy = instr.__copy__()
            for i, a in enumerate(arrangement):
                instr_copy.records[instr.unknown[i]] = '#' if a else '.'
            if instr_copy.is_valid:
                total += 1

    print(total)

