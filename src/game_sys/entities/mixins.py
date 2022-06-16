from src.game_sys.entities.entity import Bullet
import pygame

# --------------------- MIXIN CLASSES -------------------------- #

# Superclass for all shooting entities


class ShooterMixin:
    def __init__(self, reload_time, delta_time, sound = False):

        self.bullets = []
        self.reload_time = reload_time
        self.total_reload_time = self.reload_time
        self.delta_time = delta_time
        self.shoot_fx = pygame.mixer.Sound('./sound/shooting.wav')
        self.sound = sound

    def shoot(self, position, target_x, target_y, surface):
        if self.reload_time <= 0:
            self.add_bullet(position, target_x, target_y, surface)
            self.reload_time = self.total_reload_time
            if self.sound:
                self.shoot_fx.play()

    def reload(self):
        if self.reload_time > 0:
            self.reload_time -= 1

    def add_bullet(self, position, target_x, target_y, surface):
        bullet = Bullet(position[0], position[1],
                        target_x, target_y, surface, self.delta_time)
        self.bullets.append(bullet)

    def update(self):
        self.reload()
