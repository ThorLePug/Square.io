import pygame
from typing import Callable
from utils.text_system import Font, TextSurf

pygame.mixer.init()

select_sound = pygame.mixer.Sound('sound/button_select.wav')


def do_nothing():
    return ''


class Button(TextSurf):
    def __init__(self, scr_width: int, font: Font, func: Callable, y, text_displayed='',
                 interact = False, data_get = do_nothing):
        self.interact = interact
        self.data_get = data_get
        send_text = text_displayed + str(self.data_get()) if not self.interact else\
            text_displayed + ' : ' + str(self.data_get())
        TextSurf.__init__(self, send_text, font, scr_width, y)
        self.text_in = text_displayed
        self.execute = func

    def render(self, surface: pygame.Surface):
        text = self.text_in + str(self.data_get()) if not self.interact else\
            self.text_in + ' : ' + str(self.data_get())
        surface.blit(self.image, self.rect)
        self.font.render(surface, text, self.rect.topleft)

    def is_clicked(self, mouse_pos: tuple[int, int]):
        click = False
        if self.rect.collidepoint(mouse_pos):
            click = True
            select_sound.play()
        return click


class Menu:
    def __init__(self, game, buttons, text_surf: list[TextSurf] = ()):
        self.game = game
        self.WINDOW = game.WINDOW
        self.buttons = buttons
        self.text_surf = text_surf

        pygame.mouse.set_visible(True)

        self.old_press = True
        self.running = True

    def button_clicked(self, mouse_pos):
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.execute()

    def update(self):
        press = pygame.mouse.get_pressed(num_buttons=3)

        for button in self.buttons:
            button.render(self.WINDOW)

        for surf in self.text_surf:
            surf.draw(self.WINDOW)

        if press[0] and not self.old_press:
            self.button_clicked(pygame.mouse.get_pos())

        self.old_press = press[0]
