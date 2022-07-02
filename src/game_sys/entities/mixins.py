from .entity import Bullet
import pygame

# --------------------- MIXIN CLASSES -------------------------- #

# Parent class for all shooting entities


class _CanShoot:
    def __init__(self, reload_time, delta_time, sound = False):

        self.bullets = []
        self.reload_time = reload_time
        self.total_reload_time = self.reload_time
        self.delta_time = delta_time
        self.shoot_fx = pygame.mixer.Sound('sound/shooting.wav')
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


class _PowerUp:
    def __init__(self):
        ...
    # To be completed


class Shield(pygame.sprite.Sprite):
    def __init__(self, p_pos: tuple[int, int], radius = 50):
        super().__init__()
        self.image = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = list(p_pos)
        pygame.draw.circle(self.image, (0, 0, 255), (radius, radius), radius, width=1)

        self.lifespan = 60 * 5
        self.life_left = self.lifespan

    def update(self, p_position: tuple[int, int], surface: pygame.Surface):
        if self.life_left > 0:
            self.life_left -= 1
        self.rect.center = p_position
        surface.blit(self.image, self.rect)


class _CanShield:
    def __init__(self):
        self._shield = None
        self._has_shield = False
        self.cooldown = 60 * 10

    def activate_shield(self, p_position):
        if not self._has_shield and self.cooldown == 0:
            self._shield = Shield(p_position)

    def update(self, p_position, surface):
        if self._has_shield:
            self._shield.update(p_position, surface)
            if self._shield.life_left == 0:
                self._shield = None
                self._has_shield = False

        elif self.cooldown > 0:
            self.cooldown -= 1

