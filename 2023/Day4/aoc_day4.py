import fileinput, re
from copy import copy
from dataclasses import dataclass
from typing import List

lines = list(map(lambda x: x.strip(), list(fileinput.input('input.txt'))))


@dataclass
class Card:
    id: int
    winning_numbers: List[int]
    numbers: List[int]
    scratchcards_count: int = 0

    def get_scratchcards(self) -> List:
        return [copy(c) for j, c in enumerate(cards) if
                self.id < j <= self.id + self.count_matches < len(cards)] if self.count_matches else None

    @property
    def count_matches(self) -> int:
        return len([x for x in self.numbers if x in self.winning_numbers])

    def __copy__(self):
        return Card(self.id, [*self.winning_numbers], [*self.numbers], self.scratchcards_count)

    def __repr__(self):
        return str((self.id, self.count_matches))

# def count_scratchcards(card: Card) -> int:
#     scratchcards: List[Card] = card.get_scratchcards()
#     if not scratchcards:
#         return card.scratchcards_count
#     for c in scratchcards:
#         card.scratchcards_count += count_scratchcards(c) if c.count_matches else 0
#     return card.scratchcards_count

def count_scratchcards(card: Card) -> int:
    scratchcards: List[Card] = card.get_scratchcards()
    if not scratchcards:
        return card.scratchcards_count
    for c in scratchcards:
        card.scratchcards_count += count_scratchcards(c) if c.count_matches else 0
    return card.scratchcards_count

result_part1: int = 0
cards: List[Card] = []
for i, line in enumerate(lines):
    winning_numbers, numbers = line.split(':')[1].split('|')
    winning_numbers = re.findall(r'(\d+)', winning_numbers)
    numbers = re.findall(r'(\d+)', numbers)
    # print(winning_cards, hand)
    match_count = len([x for x in numbers if x in winning_numbers])
    score_part1: int = 2 ** (match_count - 1) if match_count > 0 else 0
    result_part1 += score_part1
    cards.append(Card(i, winning_numbers, numbers))

print('part 1: ', result_part1)

result_part2: int = 0
copies = {i: 1 for i in range(len(cards) + 1)}
for i, c in enumerate(cards):
    for j in range(i + 1, i + c.count_matches + 1):
        copies[j] += copies[i]
    result_part2 += copies[i]
    # result_part2 += count_scratchcards(c)

print('part 2: ', result_part2)
