import cards
import pygame
import element

# initialize
phase = 0
current_player = 0
# 'fonts/CallingCode-Regular.ttf'
static_sprites = pygame.sprite.Group()
dynamic_sprites = pygame.sprite.Group()
card_sprites = pygame.sprite.Group()
dynamic_elements = []

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Poker')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in dynamic_elements:
                if i.is_hovered():
                    for q in dynamic_elements:
                        q.unselect()
                    i.click()

    if phase == 0:
        background = element.UiElement("images/PokerTable.jpg", 0, 0, 1280, 720)
        static_sprites.add(background.sprite)
        # create main menu
        menu_background = element.UiElement("images/main-menu-background.png", 300, 20, 680, 680)
        static_sprites.add(menu_background.sprite)
        welcome_text = element.TextElement('Welcome To Poker!', 'fonts/CallingCode-Regular.ttf', 52, 640, 50)
        static_sprites.add(welcome_text.sprite)
        num_players_text = element.TextElement("Select The Number of Players:", 'fonts/CallingCode-Regular.ttf', 36, 640, 150)
        static_sprites.add(num_players_text.sprite)
        # num players buttons
        for i in element.create_num_player_buttons():
            dynamic_elements.append(i)
            dynamic_sprites.add(i.sprite)

        phase += 1
    elif phase == 1:
        for i in dynamic_elements:
            if i.tracked_bool:
                game_state = cards.GameState(10000, 5, i.id + 3)
                phase += 1
    # EVENTS
    # Start of game
    elif phase == 2:
        # delete menu elements
        static_sprites.remove(static_sprites.sprites()[1:])
        dynamic_sprites.remove(dynamic_sprites.sprites())
        dynamic_elements = []

        # create ui elements
        for i in element.create_player_icons(game_state.num_players, game_state.players):
            static_sprites.add(i.sprite)

        phase += 1

    elif phase == 3:
        if current_player == 0:
            if len(dynamic_elements) == 0:
                for i in element.create_player_option_buttons():
                    dynamic_elements.append(i)
                    dynamic_sprites.add(i.sprite)
            else:
                for i in dynamic_elements:
                    if i.tracked_bool:
                        game_state.select_player_option(current_player, i.id)




    elif phase == 4:
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
    elif phase == 3:
        for i in range(0, game_state.num_players):
            game_state.deal_to_player(i, 2)
        phase += 1
    # Go around with bets
    elif phase == 4:
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
    elif phase == 5:
        game_state.add_to_river(3)
        phase += 1
    # Go around with bets
    elif phase == 6:
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
    elif phase == 7:
        game_state.add_to_river(1)
        phase += 1
    # Go around with bets
    elif phase == 8:
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
    elif phase == 9:
        game_state.add_to_river(1)
        phase += 1
    # Go around with bets
    elif phase == 10:
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
    elif phase == 11:
        game_state.determine_winner()
        # running = False

    # draw the sprites to the window
    static_sprites.draw(screen)
    dynamic_sprites.draw(screen)

    # update the screen
    pygame.display.update()

