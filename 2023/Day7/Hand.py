from dataclasses import dataclass
from typing import List
from constants import card_values, list_functions
import unittest

@dataclass
class Hand:
    hand: List[str]
    bid: int

    @property
    def value(self):
        return max([f(self.hand) for f in list_functions])

    def __lt__(self, other):
        if self.value == other.value:
            # print(f'comparing {self.hand} and {other.hand}')
            hand_1 = list(self.hand)
            hand_2 = list(other.hand)
            while hand_1:
                card_1 = hand_1.pop(0)
                card_2 = hand_2.pop(0)
                if card_1 != card_2:
                    return card_values.index(card_1) < card_values.index(card_2)
        return self.value < other.value

    def __repr__(self):
        return f'({self.hand} {self.bid} {self.value})'


