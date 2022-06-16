import pygame

# ---- FADEOUT --------


class Fader:
    def __init__(self):
        self.alpha = 0
        self.alpha_surf = pygame.Surface((640, 640))
        self.alpha_surf.set_alpha(self.alpha)

    def fade(self, surface: pygame.Surface):
        self.alpha += 3
        self.alpha_surf.set_alpha(self.alpha)
        surface.blit(self.alpha_surf, (0, 0))




