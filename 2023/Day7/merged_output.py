# Imports
from dataclasses import dataclass

from functions import *


# Function and Class Declarations


@dataclass
class Hand:
    hand: List[str]
    bid: int

    @property
    def value(self):
        return max([f(self.hand) for f in list_functions])

    def __lt__(self, other):
        if self.value == other.value:
            print(f'comparing {self.hand} and {other.hand}')
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


def five_of_a_kind(hand: List[str]) -> int:
    return 6 if hand[0] == hand[1] == hand[2] == hand[3] == hand[4] else -1


def four_of_a_kind(hand: List[str]) -> int:
    uniq_cards = list(set(hand))
    for card in uniq_cards:
        if hand.count(card) == 4:
            return 5
    return -1


def full_house(hand: List[str]) -> int:
    uniq_cards = list(set(hand))
    count: int = 0
    for card in uniq_cards:
        if hand.count(card) == 3:
            count += 3
        if hand.count(card) == 2:
            count += 2
    return -1 if count != 5 else 4


def three_of_a_kind(hand: List[str]) -> int:
    uniq_cards = list(set(hand))
    for card in uniq_cards:
        if hand.count(card) == 3:
            return 3
    return -1


def two_pairs(hand: List[str]) -> int:
    uniq_cards = list(set(hand))
    count: int = 0
    for card in uniq_cards:
        if hand.count(card) == 2:
            count += 2
    return -1 if count != 4 else 2


def one_pair(hand: List[str]) -> int:
    uniq_cards = list(set(hand))
    for card in uniq_cards:
        if hand.count(card) == 2:
            return 1
    return -1


def high_card(hand: List[str]) -> int:
    return 0 if len(set(hand)) == 5 else -1


card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

list_functions: List = [five_of_a_kind, four_of_a_kind, full_house, three_of_a_kind, two_pairs, one_pair, high_card]

if __name__ == "__main__":
    with open('input.txt') as f:
        lines = f.read().split("\n")

    hands: List[Hand] = []
    for line in lines:
        hand, bid = line.split(" ")
        bid = int(bid)
        hands.append(Hand(hand, bid))

    hands.sort()
    print(hands)

    total: int = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid

    print(total)
