import pygame
from window import GameWindow

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    window = GameWindow()
    window.main()
