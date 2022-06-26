import pygame


class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../img/pointer.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, pos_x, pos_y):
        self.rect.center = (pos_x, pos_y)
