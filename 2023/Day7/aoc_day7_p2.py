import sys
from copy import copy
from dataclasses import dataclass
from typing import List


def debug(*args):
    # return
    print(*args, file=sys.stderr)
    sys.stderr.flush()


class Hand:
    hand: List[str]
    bid: int
    true_hand: List[str] = []

    def __init__(self, hand: List[str], bid: int):
        self.bid = bid
        self.true_hand = copy(hand)
        jokers_count = hand.count('J')
        match jokers_count:
            case 5:
                self.hand = ['A'] * 5
            case 4:
                # 4 Jokers : Quinte de la valeur de la 5ème carte
                self.hand = [c for c in hand if c != 'J'] * 5
            case 3:
                # 3 Jokers : si 2 autres cartes identiques -> Quinte, sinon Carré
                true_cards = [c for c in hand if c != 'J']
                if len(set(true_cards)) == 2:
                    higher_card = max(true_cards, key=lambda c: card_values.index(c))
                    lower_card = min(true_cards, key=lambda c: card_values.index(c))
                    pos_lower_card = hand.index(lower_card)
                    self.hand = [''] * 5
                    for i in range(5):
                        if i == pos_lower_card:
                            self.hand[i] = lower_card
                        else:
                            self.hand[i] = higher_card
                else:
                    self.hand = [true_cards[0]] * 5
            case 2:
                max_value = 0
                pos_first_joker = hand.index('J')
                pos_second_joker = hand.index('J', pos_first_joker + 1)
                for c1 in card_values[1:]:
                    for c2 in card_values[1:]:
                        new_hand = [''] * 5
                        for i in range(5):
                            if i == pos_first_joker:
                                new_hand[i] = c1
                            elif i == pos_second_joker:
                                new_hand[i] = c2
                            else:
                                new_hand[i] = hand[i]
                        hand_value = max([f(new_hand) for f in list_functions])
                        if hand_value > max_value:
                            self.hand = new_hand
                            max_value = hand_value
            case 1:
                max_value = 0
                pos_joker = hand.index('J')
                for c in card_values[1:]:
                    new_hand = [''] * 5
                    for i in range(5):
                        if i == pos_joker:
                            new_hand[i] = c
                        else:
                            new_hand[i] = hand[i]
                    hand_value = max([f(new_hand) for f in list_functions])
                    if hand_value > max_value:
                        self.hand = new_hand
                        max_value = hand_value
            case 0:
                self.hand = hand
        # debug(f'{jokers_count} Joker(s): {self.true_hand} - {self.hand}')

    @property
    def value(self):
        return max([f(self.hand) for f in list_functions])

    def __lt__(self, other):
        if self.value == other.value:
            hand_1 = list(self.true_hand)
            hand_2 = list(other.true_hand)
            while hand_1:
                card_1 = hand_1.pop(0)
                card_2 = hand_2.pop(0)
                if card_1 != card_2:
                    # if card_values.index(card_1) < card_values.index(card_2):
                    #     debug(f'{self.hand} < {other.hand}')
                    # else:
                    #     debug(f'{self.hand} > {other.hand}')
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


old_card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
card_values = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
list_functions: List = [five_of_a_kind, four_of_a_kind, full_house, three_of_a_kind, two_pairs, one_pair, high_card]

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
