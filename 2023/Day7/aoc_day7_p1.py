import Hand
from functions import *

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
