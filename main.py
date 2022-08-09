import cards
import pygame

phase = 0
current_player = 0

pygame.init()
screen = pygame.display.set_mode((539, 360))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Table_img = pygame.image.load('images/PokerTable.jpg')
    screen.blit(Table_img, [0, 0])
    if phase == 0:
        game_state = cards.GameState(1000, 5, 4)
        phase += 1

    # EVENTS
    # Start of game
    elif phase == 1:
        # Little Blind
        if game_state.players[current_player].aspect == "little blind":
            game_state.add_bet(game_state.little_blind, current_player)
            current_player += 1
        # big blind
        elif game_state.players[current_player].aspect == "big blind":
            game_state.add_bet(game_state.little_blind * 2, current_player)
            current_player += 1
        # Match Bets until dealer does
        elif game_state.players[current_player].aspect == "dealer":
            game_state.add_bet(game_state.little_blind * 2, current_player)
            current_player = 0
            phase += 1
        else:
            game_state.add_bet(game_state.little_blind * 2, current_player)
            current_player += 1
    # Deal
    elif phase == 2:
        for i in range(0, game_state.num_players):
            game_state.deal_to_player(i, 2)
        phase += 1
    # Go around with bets
    elif phase == 3:
        if game_state.players[current_player].aspect == "dealer":
            game_state.add_bet(50, current_player)
            phase += 1
            current_player = 0
        elif current_player == 0:
            # placeholder for asking player for bet/fold/check
            game_state.add_bet(50, current_player)
            current_player += 1
        else:
            # placeholder for pausing for 1 sec, determining hand value, and making decision based on that
            game_state.add_bet(50, current_player)
            current_player += 1
    # Deal the flop (three cards)
    elif phase == 4:
        game_state.add_to_river(3)
        phase += 1
    # Go around with bets
    elif phase == 5:
        if game_state.players[current_player].aspect == "dealer":
            game_state.add_bet(50, current_player)
            phase += 1
            current_player = 0
        elif current_player == 0:
            # placeholder for asking player for bet/fold/check
            game_state.add_bet(50, current_player)
            current_player += 1
        else:
            # placeholder for pausing for 1 sec, determining hand value, and making decision based on that
            game_state.add_bet(50, current_player)
            current_player += 1
    # Deal the turn (one card)
    elif phase == 6:
        game_state.add_to_river(1)
        phase += 1
    # Go around with bets
    elif phase == 7:
        if game_state.players[current_player].aspect == "dealer":
            game_state.add_bet(50, current_player)
            phase += 1
            current_player = 0
        elif current_player == 0:
            # placeholder for asking player for bet/fold/check
            game_state.add_bet(50, current_player)
            current_player += 1
        else:
            # placeholder for pausing for 1 sec, determining hand value, and making decision based on that
            game_state.add_bet(50, current_player)
            current_player += 1
    # Deal the river (one card)
    elif phase == 8:
        game_state.add_to_river(1)
        phase += 1
    # Go around with bets
    elif phase == 9:
        if game_state.players[current_player].aspect == "dealer":
            game_state.add_bet(50, current_player)
            phase += 1
            current_player = 0
        elif current_player == 0:
            # placeholder for asking player for bet/fold/check
            game_state.add_bet(50, current_player)
            current_player += 1
        else:
            # placeholder for pausing for 1 sec, determining hand value, and making decision based on that
            game_state.add_bet(50, current_player)
            current_player += 1
    # Determine winner and distribute pot
    elif phase == 10:
        game_state.determine_winner()
        #running = False


