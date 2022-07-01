"""
This module defines the Player class:
 - Parent class is Sprite.Entity
 - Controllable
"""
import pygame
from .mixins import ShooterMixin
from .entity import Entity, Shield


# --------------------- PLAYER CLASS -------------------------- #


class Player(ShooterMixin, Entity):
    def __init__(self, surface, delta_fps):
        Entity.__init__(self, width=44, height=44, pos_x=90, pos_y=90,
                        speed=4, colour=(0, 0, 255), surface=surface, delta_fps=delta_fps, health=50)
        ShooterMixin.__init__(self, reload_time=10, delta_time=delta_fps, sound=True)

        self.shield = None
        self.power_up = pygame.sprite.Group()

        self.has_shield = False
        self.shield_timer = 60 * 5
        self.shield_time_left = self.shield_timer

        self.old_position = self.position.copy()

    def save_position(self):
        self.old_position = self.position.copy()

    def get_shield(self):
        if not self.has_shield:
            self.has_shield = True
            self.shield = Shield(self.position)
            self.power_up.add(self.shield)

    def check_power_up(self):
        self.power_up.update(self.position)
        self.power_up.draw(self.surface)
        if self.has_shield:
            if self.shield_time_left > 0:
                self.shield_time_left -= 1
            else:
                self.shield.kill()
                self.has_shield = False
                self.shield_time_left = self.shield_timer

    def update(self):
        self.check_power_up()

        Entity.update(self)
        ShooterMixin.update(self)

        for bullet in self.bullets:
            bullet.update()
            self.surface.blit(bullet.image, bullet.rect.center)

    def move_back(self):
        self.position = self.old_position
        Entity.update(self)

    def disappear(self):
        Entity.disappear(self)
        self.power_up.empty()

# Entity Inheritance --> modified movement + update overload
