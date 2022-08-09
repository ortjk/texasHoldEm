import pygame


class UiElement:
    def __init__(self, img_path, x, y, width, height):
        self.e_sprite = pygame.sprite.Sprite()
        self.e_sprite.image = pygame.transform.scale(pygame.image.load(img_path), (width, height))
        self.e_sprite.rect = self.e_sprite.image.get_rect()
        self.e_sprite.rect.topleft = (x, y)
