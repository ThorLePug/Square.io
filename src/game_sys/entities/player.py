"""
This module defines the Player class:
 - Parent class is Sprite.Entity
 - Controllable
"""
from .mixins import _CanShoot, _CanShield
from .entity import Entity


# --------------------- PLAYER CLASS -------------------------- #

class Player(Entity, _CanShoot, _CanShield):
    width = 44
    height = 44
    colour = (0, 0, 255)
    speed = 4
    health = 60

    def __init__(self, surface, delta_fps):
        Entity.__init__(self, pos_x=90, pos_y=90, surface=surface, delta_fps=delta_fps)
        _CanShoot.__init__(self, reload_time=10, delta_time=delta_fps, sound=True)
        _CanShield.__init__(self)

        self.old_position = self.position.copy()

    def save_position(self):
        self.old_position = self.position.copy()

    def update(self):
        Entity.update(self)
        _CanShoot.update(self)
        _CanShield.update(self, self.position, self.surface)

    def move_back(self):
        self.position = self.old_position
        Entity.update(self)
