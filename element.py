import pygame
import spritesheet


def retrieve_from_ss(img_path, x, y, width, height):
    ss = spritesheet.spritesheet(img_path)
    return ss.image_at((x, y, width, height))


def create_num_player_buttons():
    elems = []
    for i in range(0, 8):
        if i <= 3:
            x = retrieve_from_ss("images/PlayerNumbers.png", 59 * i + 26, 8, 52, 73)
            num_players_btn = ButtonFromImage(x, 86 * i + 500, 180, 52, 73, i)
        else:
            x = retrieve_from_ss("images/PlayerNumbers.png", 59 * (i - 4) + 26, 88, 52, 73)
            num_players_btn = ButtonFromImage(x, 86 * (i - 4) + 500, 264, 52, 73, i)
        elems.append(num_players_btn)
    return elems


def create_player_option_buttons():
    elems = []
    for i in range(0, 4):
        x = retrieve_from_ss("images/buttons.jpeg", 56, i * 119 + 54, 165, 47)
        btn = ButtonFromImage(x, i * 175 + 575, 673, 165, 47, i)
        elems.append(btn)
    return elems


def create_player_icons(num_players, players):
    player_icon_locations = {
        0: [475, 75],
        1: [200, 125],
        2: [125, 300],
        3: [150, 450],
        4: [475, 500],
        5: [725, 500],
        6: [975, 450],
        7: [1050, 300],
        8: [975, 125],
        9: [725, 75],
    }

    card_ss_values = {
        'spades': 11,
        'hearts': 188,
        'diamonds': 368,
        'clubs': 548,
        'ace': 11,
        'two': 129
    }

    elems = []
    for i in range(0, num_players):
        icon = UiElement(f"images/{i + 1}.png", player_icon_locations[i][0], player_icon_locations[i][1], 75, 75)
        elems.append(icon)
        player_name = TextElement(f"Player {i + 1}", "fonts/CallingCode-Regular.ttf", 32, player_icon_locations[i][0] + 35, player_icon_locations[i][1] - 25)
        elems.append(player_name)

    # separate for loop bc text must be on top
    for i in range(0, num_players):
        balance_text = TextElement(f"${players[0].balance}", "fonts/CallingCode-Regular.ttf", 28, player_icon_locations[i][0] + 30, player_icon_locations[i][1] + 100)
        elems.append(balance_text)
    elems.append(TextElement("Pot: $0", "fonts/CallingCode-Regular.ttf", 52, 625, 275))
    return elems


class UiElement:
    def __init__(self, img_path, x, y, width, height):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.transform.scale(pygame.image.load(img_path), (width, height))
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (x, y)


class TextElement:
    def __init__(self, text, font_path, size, x, y):
        font = pygame.font.Font(font_path, size)
        text = font.render(text, True, (255, 255, 255))
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface((text.get_width(), text.get_height()))
        self.sprite.image.set_alpha(150)
        self.sprite.image.blit(text, (0, 0))

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = (x, y)


class ButtonFromImage:
    def __init__(self, img, x, y, width, height, num):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.transform.scale(img, (width, height))
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (x, y)

        self.tracked_bool = False
        self.id = num

    def is_hovered(self):
        if self.sprite.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def click(self):
        if self.tracked_bool:
            self.tracked_bool = False
        else:
            self.tracked_bool = True

    def unselect(self):
        self.tracked_bool = False



