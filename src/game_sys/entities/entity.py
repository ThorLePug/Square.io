import pygame
import math


class Entity(pygame.sprite.Sprite):
    width = 20
    height = 20
    speed = 2
    colour = (0, 0, 0)
    health = 10

    def __init__(self, x, y, surface, delta_fps):
        super().__init__()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()

        self.position = [x, y]
        self.rect.center = self.position
        self.speed = self.speed * delta_fps
        self.delta_fps = delta_fps

        self.health = self.health
        self.total_health = self.health

        self.scale = 1.0
        self.surface = surface

        self.is_killed = False

    def move(self, direction, pixels=0):
        if direction == 'down':
            self.position[1] += pixels
        if direction == 'up':
            self.position[1] -= pixels
        if direction == 'left':
            self.position[0] -= pixels
        if direction == 'right':
            self.position[0] += pixels

    def update(self):
        self.rect.center = self.position
        if self.health <= 0:
            self.is_killed = True
        if self.is_killed:
            self.disappear()

    def disappear(self):
        if self.scale > 0:
            self.image = pygame.transform.scale(self.image, (int(self.rect.width * self.scale),
                                                             int(self.rect.height * self.scale)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.scale -= 0.05 * self.delta_fps
        else:
            self.kill()


# --------------------- BULLET CLASS -------------------------- #
# Basic bullet used by Player and Enemy


class Bullet(Entity):
    width = 8
    height = 8
    speed = 8
    colour = (255, 0, 0)
    health = 1

    def __init__(self, x, y, target_x, target_y, surface, origin, delta_fps=1):
        Entity.__init__(self, x=x, y=y, surface=surface, delta_fps=delta_fps)

        self.initial_pos = [x, y]

        self.angle = -math.atan2(target_x - self.initial_pos[0],
                                 target_y - self.initial_pos[1]) + math.pi/2
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        self.origin = origin
        self.damage = 30

    def update(self):
        self.position[0] += self.dx
        self.position[1] += self.dy
        self.rect.center = self.position
