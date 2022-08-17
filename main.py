import cards
import pygame
import element
import random as r


def update_balance_visuals(_static_sprites, _game_state, _num_players):
    _static_sprites.remove(_static_sprites.sprites()[:-2 - _num_players:-1])
    for i in element.create_balance_text(_game_state):
        _static_sprites.add(i.sprite)


# initialize
phase = 0
current_player = 0
tentative_bet = 0

static_sprites = pygame.sprite.Group()
dynamic_sprites = pygame.sprite.Group()
card_sprites = pygame.sprite.Group()
tentative_bet_text = pygame.sprite.Group()
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
        for i in element.create_player_icons(game_state.num_players):
            static_sprites.add(i.sprite)

        for i in element.create_balance_text(game_state):
            static_sprites.add(i.sprite)

        phase += 1

    # blinds
    elif phase == 3:
        if game_state.players[current_player].aspect == "little blind":
            game_state.add_bet(game_state.little_blind, current_player)
            current_player += 1
        elif game_state.players[current_player].aspect == "big blind":
            game_state.add_bet(game_state.little_blind * 2, current_player)
            current_player += 1
        elif game_state.players[current_player].aspect == "dealer":
            game_state.add_bet(game_state.little_blind, current_player)
            current_player = 0
            phase += 1
        else:
            game_state.add_bet(game_state.little_blind * 2, current_player)
            current_player += 1

    elif phase == 4:
        # deal cards
        if current_player < game_state.num_players - 1:
            game_state.deal_to_player(current_player, 2)
            for i in element.create_player_cards(game_state.players[current_player].hand, current_player):
                card_sprites.add(i.sprite)
            current_player += 1
        else:
            game_state.deal_to_player(current_player, 2)
            for i in element.create_player_cards(game_state.players[current_player].hand, current_player):
                card_sprites.add(i.sprite)
            current_player = 0
            phase += 1

    elif phase == 5:
        if game_state.players[current_player].folded:
            if current_player < game_state.num_players - 1:
                current_player = 0
                phase += 1
            else:
                current_player += 1
        elif current_player == 0:
            if len(dynamic_elements) == 0:
                for i in element.create_player_option_buttons():
                    dynamic_elements.append(i)
                    dynamic_sprites.add(i.sprite)
            else:
                for i in dynamic_elements:
                    if i.tracked_bool:
                        if i.id <= 2:
                            game_state.select_player_option(current_player, i.id, tentative_bet)
                            current_player += 1
                            tentative_bet = 0

                            dynamic_elements = []
                            dynamic_sprites.remove(dynamic_sprites.sprites())
                        elif i.id == 3:
                            if game_state.players[current_player].balance > tentative_bet:
                                tentative_bet += 50
                            i.tracked_bool = False
                        elif i.id == 4:
                            if tentative_bet > 0:
                                tentative_bet -= 50
                            i.tracked_bool = False

        elif current_player < game_state.num_players - 1:
            game_state.select_player_option(current_player, 1, 50)
            current_player += 1
        else:
            game_state.select_player_option(current_player, 2, 50)
            current_player = 0
            phase += 1

        update_balance_visuals(static_sprites, game_state, game_state.num_players)
        tentative_bet_text.remove(tentative_bet_text.sprites())
        tentative_bet_text.add(element.TextElement(f"${tentative_bet}", 'fonts/CallingCode-Regular.ttf', 28, 1000, 650).sprite)


    elif phase == 6:
        game_state.add_to_river(3)
        for i in element.create_river_cards(game_state.river, game_state):
            card_sprites.add(i.sprite)
        phase += 1

    elif phase == 7:
        if game_state.players[current_player].folded:
            if current_player < game_state.num_players - 1:
                current_player = 0
                phase += 1
            else:
                current_player += 1
        elif current_player == 0:
            if len(dynamic_elements) == 0:
                for i in element.create_player_option_buttons():
                    dynamic_elements.append(i)
                    dynamic_sprites.add(i.sprite)
            else:
                for i in dynamic_elements:
                    if i.tracked_bool:
                        if i.id <= 2:
                            game_state.select_player_option(current_player, i.id, tentative_bet)
                            current_player += 1
                            tentative_bet = 0

                            dynamic_elements = []
                            dynamic_sprites.remove(dynamic_sprites.sprites())
                        elif i.id == 3:
                            if game_state.players[current_player].balance > tentative_bet:
                                tentative_bet += 50
                            i.tracked_bool = False
                        elif i.id == 4:
                            if tentative_bet > 0:
                                tentative_bet -= 50
                            i.tracked_bool = False

        elif current_player < game_state.num_players - 1:
            game_state.select_player_option(current_player, 1, 50)
            current_player += 1
        else:
            game_state.select_player_option(current_player, 2, 50)
            current_player = 0
            phase += 1

        update_balance_visuals(static_sprites, game_state, game_state.num_players)
        tentative_bet_text.remove(tentative_bet_text.sprites())
        tentative_bet_text.add(
            element.TextElement(f"${tentative_bet}", 'fonts/CallingCode-Regular.ttf', 28, 1000, 650).sprite)

    elif phase == 8:
        game_state.add_to_river(1)
        for i in element.create_river_cards(game_state.river, game_state):
            card_sprites.add(i.sprite)
        phase += 1

    elif phase == 9:
        if game_state.players[current_player].folded:
            if current_player < game_state.num_players - 1:
                current_player = 0
                phase += 1
            else:
                current_player += 1
        elif current_player == 0:
            if len(dynamic_elements) == 0:
                for i in element.create_player_option_buttons():
                    dynamic_elements.append(i)
                    dynamic_sprites.add(i.sprite)
            else:
                for i in dynamic_elements:
                    if i.tracked_bool:
                        if i.id <= 2:
                            game_state.select_player_option(current_player, i.id, tentative_bet)
                            current_player += 1
                            tentative_bet = 0

                            dynamic_elements = []
                            dynamic_sprites.remove(dynamic_sprites.sprites())
                        elif i.id == 3:
                            if game_state.players[current_player].balance > tentative_bet:
                                tentative_bet += 50
                            i.tracked_bool = False
                        elif i.id == 4:
                            if tentative_bet > 0:
                                tentative_bet -= 50
                            i.tracked_bool = False

        elif current_player < game_state.num_players - 1:
            game_state.select_player_option(current_player, 1, 50)
            current_player += 1
        else:
            game_state.select_player_option(current_player, 2, 50)
            current_player = 0
            phase += 1

        update_balance_visuals(static_sprites, game_state, game_state.num_players)
        tentative_bet_text.remove(tentative_bet_text.sprites())
        tentative_bet_text.add(
            element.TextElement(f"${tentative_bet}", 'fonts/CallingCode-Regular.ttf', 28, 1000, 650).sprite)

    elif phase == 10:
        game_state.add_to_river(1)
        for i in element.create_river_cards(game_state.river, game_state):
            card_sprites.add(i.sprite)
        phase += 1

    elif phase == 11:
        if game_state.players[current_player].folded:
            if current_player < game_state.num_players - 1:
                current_player = 0
                phase += 1
            else:
                current_player += 1
        elif current_player == 0:
            if len(dynamic_elements) == 0:
                for i in element.create_player_option_buttons():
                    dynamic_elements.append(i)
                    dynamic_sprites.add(i.sprite)
            else:
                for i in dynamic_elements:
                    if i.tracked_bool:
                        if i.id <= 2:
                            game_state.select_player_option(current_player, i.id, tentative_bet)
                            current_player += 1
                            tentative_bet = 0

                            dynamic_elements = []
                            dynamic_sprites.remove(dynamic_sprites.sprites())
                        elif i.id == 3:
                            if game_state.players[current_player].balance > tentative_bet:
                                tentative_bet += 50
                            i.tracked_bool = False
                        elif i.id == 4:
                            if tentative_bet > 0:
                                tentative_bet -= 50
                            i.tracked_bool = False

        elif current_player < game_state.num_players - 1:
            game_state.select_player_option(current_player, 1, 50)
            current_player += 1
        else:
            game_state.select_player_option(current_player, 2, 50)
            current_player = 0
            phase += 1

        update_balance_visuals(static_sprites, game_state, game_state.num_players)
        tentative_bet_text.remove(tentative_bet_text.sprites())
        tentative_bet_text.add(
            element.TextElement(f"${tentative_bet}", 'fonts/CallingCode-Regular.ttf', 28, 1000, 650).sprite)

    # Determine winner and distribute pot
    elif phase == 12:
        game_state.determine_winner()
        game_state.new_round_reset()
        update_balance_visuals(static_sprites, game_state, game_state.num_players)
        card_sprites.remove(card_sprites.sprites())
        phase = 3

    # draw the sprites to the window
    static_sprites.draw(screen)
    dynamic_sprites.draw(screen)
    card_sprites.draw(screen)
    tentative_bet_text.draw(screen)

    # update the screen
    pygame.display.update()

