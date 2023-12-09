from typing import List
import unittest


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



