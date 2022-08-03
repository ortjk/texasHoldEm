import cards
import player
import calculations
import pygame

# init deck
deck = cards.reset_deck()

pot = 0
phase = 0
current_player = 0

pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if phase == 0:
        # placeholder for selecting starting amounts
        stack = 1000
        little_blind = 5
        num_players = 4

        # init players
        players = []
        for i in range(0, num_players):
            if i <= 1:
                players.append(player.Player(player.aspects[i], stack))
            else:
                players.append(player.Player(None, stack))
        players.append(player.Player(player.aspects[2], stack))

        phase += 1

    # EVENTS
    # Start of game
    elif phase == 1:
        # Little Blind
        if players[current_player].aspect == "little blind":
            players[current_player].bet(0 - little_blind)
            current_player += 1
        # big blind
        elif players[current_player].aspect == "big blind":
            players[current_player].bet(0 - little_blind * 2)
            current_player += 1
        # Match Bets until dealer does
        elif players[current_player].aspect == "dealer":
            players[current_player].bet(0 - little_blind * 2)
            current_player = 0
            phase += 1
        else:
            players[current_player].bet(0 - little_blind * 2)
            current_player += 1
    # Deal
    elif phase == 2:
        for i in range(0, num_players):
            players[i].deal_cards([deck[0], deck[1]])
            deck.pop(0)
            deck.pop(0)
        phase += 1
    # Go around with bets
    elif phase == 3:
        if current_player == 0:
            # placeholder for asking player for bet/fold/check
            players[current_player].bet(50)
        else:
            # placeholder for pausing for 1 sec, determining hand value, and making decision based on that
            players[current_player].bet(50)

    #
    # Deal the flop (three cards)
    # Go around with bets
    #
    # Deal the turn (one card)
    # Go around with bets
    #
    # Deal the river (one card)
    # Go around with bets
    #
    # Determine winner and distribute pot


