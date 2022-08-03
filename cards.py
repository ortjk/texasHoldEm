import random
suits = ["hearts", "diamonds", "spades", "clubs"]
ranks = {
    "two": 1,
    "three": 2,
    "four": 3,
    "five": 4,
    "six": 5,
    "seven": 6,
    "eight": 7,
    "nine": 8,
    "ten": 9,
    "jack": 10,
    "queen": 11,
    "king": 12,
    "ace": 13
}


def reset_deck():
    deck_ = []
    for i in suits:
        for q in ranks:
            deck_.append(Card(i, q))

    random.shuffle(deck_)

    return deck_


class Card:
    # create the card, using the input suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
