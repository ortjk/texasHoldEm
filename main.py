import cards
import calculations

import random

# init deck
deck = []
for i in cards.suits:
    for q in cards.ranks:
        deck.append(cards.Card(i, q))

random.shuffle(deck)

