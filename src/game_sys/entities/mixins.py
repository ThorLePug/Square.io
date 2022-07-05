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
            bullet = self.add_bullet(position, target_x, target_y, surface)
            self.reload_time = self.total_reload_time
            if self.sound:
                self.shoot_fx.play()
            return bullet

    def add_bullet(self, position, target_x, target_y, surface) -> Bullet:
        bullet = Bullet(position[0], position[1],
                        target_x, target_y, surface, self, self.delta_time)
        self.bullets.append(bullet)
        return bullet

    def update(self):
        if self.reload_time > 0:
            self.reload_time -= 1


class Shield(pygame.sprite.Sprite):
    def __init__(self, p_pos: tuple[int, int], radius = 40):
        super().__init__()
        self.radius = radius
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
        self.shield = None
        self.has_shield = False
        self.def_cooldown = 60 * 7
        self.cooldown = 0

    def activate_shield(self, p_position, radius = 40):
        if not self.has_shield and self.cooldown == 0:
            self.shield = Shield(p_position, radius)
            self.has_shield = True

    def update(self, p_position, surface):
        if self.has_shield:
            self.shield.update(p_position, surface)
            if self.shield.life_left == 0:
                self.shield = None
                self.has_shield = False
                self.cooldown = self.def_cooldown

        elif self.cooldown > 0:
            self.cooldown -= 1
