import pygame
import math


class Entity(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, speed, colour, surface, delta_fps, health):
        super().__init__()
        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color(colour))

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.position = [pos_x, pos_y]
        self.rect.center = self.position
        self.speed = speed * delta_fps
        self.delta_fps = delta_fps

        self.health = health
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
        if self.is_killed:
            self.disappear()

    def disappear(self):
        if self.scale > 0:
            self.image = pygame.transform.scale(self.image, (int(self.width * self.scale),
                                                             int(self.height * self.scale)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.scale -= 0.05 * self.delta_fps
        else:
            self.kill()


# --------------------- BULLET CLASS -------------------------- #
# Basic bullet used by Player and Enemy


class Bullet(Entity):
    def __init__(self, pos_x, pos_y, target_x, target_y, surface, delta_fps=1):
        Entity.__init__(self, width=8, height=8, pos_x=pos_x, pos_y=pos_y,
                        speed=8, colour=(255, 0, 0), surface=surface, delta_fps=delta_fps, health=1)

        self.initial_pos = [pos_x, pos_y]

        self.angle = -math.atan2(target_x - self.initial_pos[0],
                                 target_y - self.initial_pos[1]) + math.pi/2
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        self.damage = 30

    def update(self):
        self.position[0] += self.dx
        self.position[1] += self.dy
        self.rect.center = self.position

# --------------------- SHIELD CLASS -------------------------- #
# Basic shield class for Player


class Shield(pygame.sprite.Sprite):
    def __init__(self, position: list, timer = 60*60):
        super().__init__()
        self.radius = 50
        self.final_radius = 50
        self.position = position

        self.image = pygame.Surface((10 * self.radius, 10 * self.radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (0, 0, 255), self.rect.center,
                           self.radius, width = 1)

        self.time_active = timer

    def update(self, p_position):
        self.position = p_position
        self.rect.center = self.position

