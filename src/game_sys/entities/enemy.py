import pygame
import math
from random import randint
from src.game_sys.entities.entity import Entity
from src.game_sys.entities.mixins import ShooterMixin

# --------------------- ENEMY CLASSES -------------------------- #


class Enemy(Entity):
    def __init__(self, window_width, window_height, all_sprites, walls, surface, delta_fps, width=30, height=30,
                 colour=(255, 0, 0)):
        Entity.__init__(self, width=width, height=height, pos_x= 1000, pos_y=1000, speed=2, colour=colour,
                        surface=surface, delta_fps=delta_fps, health=30)
        self.position = self.spawn(window_width, window_height, all_sprites, walls)

        # movement_area = [[self.position[0] - 10, self.position[1] - 10]
        # [self.position[0] + 10, self.position[1] + 10]]

    def spawn(self, window_width, window_height, all_sprites: pygame.sprite.Group, walls: list[pygame.Rect]):
        x = randint(50, window_width - 50)
        y = randint(50, window_height - 50)
        test_rect = self.rect.copy()

        test_rect.x, test_rect.y = (x, y)

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
        return x, y


class EnemyShooter(Enemy, ShooterMixin):
    def __init__(self, window_width, window_height, all_sprites, walls, surface, delta_fps, colour=(0, 255, 255),
                 reload_time=180, width=30, height=30):
        Enemy.__init__(self, width=width, height=height, window_width=window_width, window_height=window_height,
                       all_sprites=all_sprites, walls=walls, surface=surface, colour=colour, delta_fps=delta_fps)
        ShooterMixin.__init__(self, reload_time=reload_time, delta_time=delta_fps)

    def update(self):
        Entity.update(self)
        ShooterMixin.update(self)
        for bullet in self.bullets:
            bullet.update()
            self.surface.blit(bullet.image, bullet.rect.center)


class SpiralShooter(EnemyShooter):
    def __init__(self, window_width, window_height, all_sprites, walls, surface, delta_fps):
        EnemyShooter.__init__(self, window_width, window_height, all_sprites=all_sprites,
                              walls=walls, surface=surface, colour=(100, 100, 100), reload_time= randint(15, 45),
                              delta_fps=delta_fps)

        self.shooting_angle = 0
        self.colour = (100, 100, 0)

        self.target_x, self.target_y = self.target_definition()

    def shoot_angle_mod(self):
        if self.shooting_angle != 2 * math.pi:
            self.shooting_angle += math.pi/4
        else:
            self.shooting_angle = 0

        self.target_x, self.target_y = self.target_definition()

    def target_definition(self):
        target_x = self.position[0] + math.cos(self.shooting_angle) * 10
        target_y = self.position[1] + math.sin(self.shooting_angle) * 10

        return target_x, target_y

    def update(self):
        self.shoot_angle_mod()
        EnemyShooter.update(self)


class BossMonster(EnemyShooter):
    def __init__(self, window_width, window_height, all_sprites, walls, surface, delta_fps):
        EnemyShooter.__init__(self, window_width, window_height, all_sprites=all_sprites,
                              walls=walls, surface=surface, colour=(255, 255, 255), reload_time= randint(15, 45),
                              delta_fps=delta_fps, width=60, height=60)


