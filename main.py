import cards
import calculations
import random
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# init deck
deck = []
for i in cards.suits:
    for q in cards.ranks:
        deck.append(cards.Card(i, q))

random.shuffle(deck)
print("hello world")
