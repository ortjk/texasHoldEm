import cards

# init deck
deck = []
for i in cards.suits:
    for q in cards.ranks:
        deck.append(cards.Card(i, q))
