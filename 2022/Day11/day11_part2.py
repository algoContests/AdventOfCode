import os
from collections import deque
from dataclasses import dataclass
from time import perf_counter

@dataclass
class Monkey:
    id: int
    items: deque[int]
    divisor: int   # divisibility test's number
    true_test: int  # monkey number to send item if div_test is true
    false_test: int # monkey number to send item if div_test is false
    op_num: int
    op: str
    inspections: int

    def operation(self, item: int):
        if self.op_num:
            return (self.op_num * item) % lcf if self.op == '*' else (self.op_num + item) % lcf
        else:
            return (self.op_num ** 2) % lcf
    def __repr__(self):
        return f'Monkey #{self.id} {str(self.items)} / {self.divisor} true -> {self.true_test} false -> {self.false_test}'

MONKEYS = 8
monkeys = [Monkey(i, [], None, None, -1, -1, 0, inspections=0) for i in range(MONKEYS)]
if __name__ == "__main__":
    file_name = os.path.abspath(".") + "/input.txt"
    with open(file_name) as file:
        monkey = monkeys[0]
        for line in file:
            if 'Monkey' in line:
                id_monkey = int(line.split()[1].replace(':', ''))
                monkey = monkeys[id_monkey]
            elif 'Starting items: ' in line:
                line = line.replace('  Starting items: ', '').replace(' ', '')
                monkey.items = deque(map(int, line.split(',')))
            elif 'Operation' in line:
                line = line.replace('  Operation: ', '')
                if line.count('old') == 2:
                    print(f'Monkey #{monkey.id} -> lambda x: x * x')
                    monkey.op_num = None
                else:
                    op, number = line.split('=')[1].strip().split()[1:]
                    monkey.op_num = int(number)
                    monkey.op = op
                    if op == '*':
                        print(f'Monkey #{monkey.id} -> lambda x: x * {int(number)}')
                    else:
                        print(f'Monkey #{monkey.id} -> lambda x: x + {int(number)}')
            elif 'Test' in line:
                monkey.divisor = int(line.split()[-1])
            elif 'true' in line:
                monkey.true_test = int(line.split()[-1])
            elif 'false' in line:
                monkey.false_test = int(line.split()[-1])

    lcf: int = 1
    for m in monkeys:
        lcf *= m.divisor

    ROUNDS = 10000

    start = perf_counter()
    for i in range(ROUNDS):
        print(f'ROUND #{i}')
        monkeys_list = monkeys[:]
        while monkeys_list:
            m = monkeys_list.pop(0)
            print(f'Monkey {m.id} has {len(m.items)} items')
            while m.items:
                item: int = m.items.popleft()
                # print(item)
                # print(f'\tMonkey inspects an item with a worry level of {item}.')
                m.inspections += 1
                new_item: int = m.operation(item)
                # print(f'\tWorry level is multiplied by {m.op_num} to {new_item}.')
                #new_item: int = int(new_item / 3)
                # print(f'\tMonkey gets bored with item. Worry level is divided by 3 to {new_item}.')
                if new_item % m.divisor == 0:
                    dest_monkey_no: int = m.true_test
                    # print(f'\tMCurrent worry level is divisible by {m.div_test}.')
                else:
                    dest_monkey_no: int = m.false_test
                    # print(f'\tCurrent worry level is not divisible by {m.div_test}.')
                # print(f'\tItem with worry level {new_item} is thrown to monkey {dest_monkey_no}.')
                dest_monkey: Monkey = monkeys[dest_monkey_no]
                if dest_monkey.items:
                    dest_monkey.items.append(new_item)
                else:
                    dest_monkey.items = deque([new_item])
        elapsed_time = perf_counter() - start
        print(f'elapsed time = {round(elapsed_time)} s')

    for i, m in enumerate(monkeys):
        print(f'Monkey {m.id} inspected items {m.inspections} times.')

    monkeys.sort(key=lambda m: m.inspections, reverse=True)
    print(f'2 most active monkeys: {(monkeys[0].id, monkeys[1].id)}')

    monkey_business: int = monkeys[0].inspections * monkeys[1].inspections
    print(f'monkey_business = {monkey_business}')