import pygame
import math
from random import randint
from .entity import Entity
from .mixins import _CanShoot

# --------------------- ENEMY CLASSES -------------------------- #


class Enemy(Entity):
    height = 30
    width = 30
    colour = (255, 0, 0)

    def __init__(self, surface, delta_fps, x, y):
        Entity.__init__(self, width=self.__class__.width, height=self.__class__.height, pos_x=x, pos_y=y, speed=2,
                        colour=self.__class__.colour, surface=surface, delta_fps=delta_fps, health=30)

    @classmethod
    def spawn(cls, window_width, window_height, all_sprites: pygame.sprite.Group, walls: list[pygame.Rect],
              surface, delta_fps, width=30, height=30, colour=(255, 0, 0)):
        x = randint(50, window_width - 50)
        y = randint(50, window_height - 50)
        test_rect = pygame.Rect(x, y, width, height)

        rect_list = []
        for sprite in all_sprites:
            rect = sprite.rect.copy()
            rect.height += 30
            rect.width += 30
            rect.center = sprite.rect.center
            rect_list.append(rect)

        while test_rect.collidelist(walls) > -1 or test_rect.collidelist(rect_list) > -1:
            x = randint(0 + 20, window_width - 20)
            y = randint(0 + 20, window_height - 20)
            test_rect.center = (x, y)

        spawned = cls(surface=surface,
                      delta_fps=delta_fps,
                      x=x,
                      y=y)
        return spawned


class EnemyShooter(Enemy, _CanShoot):
    width = 30
    height = 30
    colour = (0, 255, 255)

    def __init__(self, surface, delta_fps, x, y, reload_time=180):
        Enemy.__init__(self, x=x, y=y, surface=surface, delta_fps=delta_fps)
        _CanShoot.__init__(self, reload_time=reload_time, delta_time=delta_fps)

    def update(self):
        Entity.update(self)

        _CanShoot.update(self)
        for bullet in self.bullets:
            bullet.update()
            self.surface.blit(bullet.image, bullet.rect.center)


class SpiralShooter(EnemyShooter):
    width = 30
    height = 30
    colour = (100, 100, 0)

    def __init__(self, surface, delta_fps, x, y):
        EnemyShooter.__init__(self, surface=surface, delta_fps=delta_fps, x=x, y=y, reload_time=randint(15, 45))

        self.shooting_angle = 0

        self.target_x, self.target_y = self.target_definition()

    def target_definition(self):
        target_x = self.position[0] + math.cos(self.shooting_angle) * 10
        target_y = self.position[1] + math.sin(self.shooting_angle) * 10

        return target_x, target_y

    def update(self):
        if self.shooting_angle != 2 * math.pi:
            self.shooting_angle += math.pi/4
        else:
            self.shooting_angle = 0

        self.target_x, self.target_y = self.target_definition()
        EnemyShooter.update(self)
