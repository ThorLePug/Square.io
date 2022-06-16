"""
This module creates a text-rendering system for pygame games.
It also adds a dedicated TextSurf class to make text rendering on large surfaces easier.
"""

import pygame


def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_rect)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
              'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
              'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
              'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9']


class Font:
    def __init__(self, img):
        self.spacing = 1
        font_image = img.convert_alpha()
        self.character_order = CHARACTERS
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_image.get_width()):
            c = font_image.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_image, x - current_char_width, 0,
                                current_char_width, font_image.get_height())
                self.characters[self.character_order[character_count]] = char_img
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['M'].get_width()

    def render(self, surf, text, pos: tuple[int, int]):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (pos[0] + x_offset, pos[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

    def get_width(self, text: str):
        width = 0
        for char in text:
            if char != ' ':
                width += self.characters[char].get_width() + self.spacing
            else:
                width += self.space_width + self.spacing
        return width


class TextSurf:
    def __init__(self, text, font: Font, scr_width, y, anchor='center'):
        self.text_in = text
        self.font = font
        self.txt_width = self.font.get_width(self.text_in)
        self.height = 35
        self.image = pygame.Surface((self.txt_width, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        if anchor == 'center':
            self.rect.center = (scr_width / 2, y)
        elif anchor == 'left':
            self.rect.topleft = (100, y)
        elif anchor == 'right':
            self.rect.topright = (scr_width - 100, y)

        self.txt_startpoint = (int(self.rect.centerx - self.txt_width / 2), int(self.rect.top))

    def draw(self, surface):
        self.font.render(surface, self.text_in, self.txt_startpoint)
