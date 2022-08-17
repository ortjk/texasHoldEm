import cards
import pygame
import element
import socket

phase = 0
current_player = 0
static_sprites = pygame.sprite.Group()
dynamic_sprites = pygame.sprite.Group()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True

#Host, beginning of file:
# get the ip address of the host
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# set up the network for the host
host = str(ip)
print(f"The host IP is: {host}")
port = 62222
c = socket.socket()
c.bind((host, port))
c.listen(1)
s, addr = c.accept()
s.settimeout(0.000001)  # prevents game lag
def ReturnHand(hand: list):
    for i in hand:
        s.send(bytes(i.rank, 'utf-8'))
        s.send(bytes(";", 'utf-8'))
        s.send(bytes(i.suit, 'utf-8'))
        s.send(bytes(";", 'utf-8'))
        print(i.rank, i.suit)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if phase == 0:
        new_sprite = element.UiElement("images/1.png", 0, 0, 100, 100)
        static_sprites.add(new_sprite.sprite)

        game_state = cards.GameState(1000, 5, 2)
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
        # normal player
        else:
            game_state.add_bet(game_state.little_blind * 2, current_player)
            current_player += 1
    # Deal
    elif phase == 2:
        for i in range(0, game_state.num_players):
            game_state.deal_to_player(i, 4)
            print(f"Player {i+1}:")
            ReturnHand(game_state.players[i].hand)
            print()

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
        # running = False

    # adds player 2's bet to the pot, trys to receive data, if there is no data at the time it passes
    try:
        data = s.recv(1024)
        data = str(data, 'utf-8')
        data = data.split(";")
        sub = 0
        for i in range(len(data)):
            if (data[i-sub] == ''):
                data.pop(i-sub)
                sub += 1
                continue
            data[i-sub] = int(data[i-sub])
        data = sum(data)
        # add's the player 2 bet's
        game_state.add_bet(data, current_player + 1)
    except:
        pass
    # draw the sprites to the window
    static_sprites.draw(screen)
    dynamic_sprites.draw(screen)

    # update the screen
    pygame.display.update()

