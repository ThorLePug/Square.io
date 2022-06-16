import pygame
from pygame.locals import *
import sys
import json
from game_sys.game import Game
from menu import Menu
from menu import Button
from utils.text_system import Font, TextSurf

# --------------------------------------------


def get_score(elem) -> int:
    return elem.get('Score')


class GameWindow:
    def __init__(self) -> None:

        # Base WINDOW setup
        self.WINDOW = pygame.display.set_mode((640, 640))
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 640
        pygame.display.set_caption('Square.io')
        pygame.display.set_icon(pygame.image.load('./img/Logo.png'))

        # Menu : Title img
        self.title_img = pygame.image.load('./img/game_title.png')
        self.title_rect = self.title_img.get_rect()
        self.title_rect.center = (320, 130)

        # Base FPS counter
        self.fps = 60

        # Load fonts
        self.text_font = Font(pygame.image.load('./img/large_pygame_font.png'))
        self.title_font = Font(pygame.image.load('./img/titles_pygame_font.png'))

        # Music setup
        self.STATUS = ['OFF', 'ON']
        self.game_music_on = 1
        self.music_status = self.STATUS[self.game_music_on]

        # Prepare Buttons for MENU SETUP
        play_button = Button(self.WINDOW_WIDTH, self.title_font, self.start_game, 300,
                             'PLAY')
        settings_button = Button(self.WINDOW_WIDTH, self.title_font, self.go_settings, 350,
                                 'SETTINGS')
        leaderboard_button = Button(self.WINDOW_WIDTH, self.title_font, self.go_leaderboard, 400, 'LEADERBOARD')
        quit_button = Button(self.WINDOW_WIDTH, self.title_font, self.close_window, 450,
                             'QUIT')
        fps_button = Button(self.WINDOW_WIDTH, self.title_font, self.set_fps, 250,
                            'FPS', interact=True, data_get=self.get_fps)
        music_button = Button(self.WINDOW_WIDTH, self.title_font, self.set_music, 300, 'MUSIC', interact=True,
                              data_get=self.get_music)
        menu_button = Button(self.WINDOW_WIDTH, self.title_font, self.go_menu, 350,
                             'Return')

        # Load LEADERBOARD from JSON
        self.leaderboard = self.load_data()

        # Main Game Pages Setup
        self.game = None
        self.main_menu = Menu(self, buttons=[play_button, settings_button, leaderboard_button, quit_button])
        self.settings_menu = Menu(self, buttons=[fps_button, menu_button, music_button])
        self.leader_board = None

        # Check status
        self.status = {
            'in_game': False,
            'in_menu': True,
            'in_settings': False,
            'in_leaderboard': False
        }

    @staticmethod
    def load_data() -> list[dict]:
        with open('./data/leaderboard.json', 'r') as f:
            return json.load(f)

    def start_game(self) -> None:  # Method to begin game loop (game update in loop)
        game = Game(self)
        for item in self.status.keys():
            if item == 'in_game':
                self.status[item] = True
            else:
                self.status[item] = False
        self.game = game
        self.game.enemy_setup()
        pygame.mouse.set_visible(False)

    def go_menu(self) -> None:  # Method to begin menu loop (update in loop)
        pygame.mouse.set_visible(True)
        for item in self.status.keys():
            if item == 'in_menu':
                self.status[item] = True
            else:
                self.status[item] = False

    def go_settings(self) -> None:  # Method to begin settings loop (update in loop)
        for item in self.status.keys():
            if item == 'in_settings':
                self.status[item] = True
            else:
                self.status[item] = False

    def go_leaderboard(self) -> None:  # Method to set up leaderboard UI
        menu_button2 = Button(self.WINDOW_WIDTH, self.title_font, self.go_menu, 600, 'Return')
        lead_surf = TextSurf('LEADERBOARD', self.title_font, self.WINDOW_WIDTH, 50)
        self.leaderboard.sort(key=get_score, reverse=True)

        y_offset = 0
        lead_list = [lead_surf]
        for i in range(9):
            if i < len(self.leaderboard):
                player = self.leaderboard[i]
                name = str(player['Name'])
                score = str(player['Score'])
                name_surf = TextSurf(name, self.title_font, self.WINDOW.get_width(), 100 + y_offset, anchor='left')
                score_surf = TextSurf(score, self.title_font, self.WINDOW.get_width(), 100 + y_offset, anchor='right')
                lead_list.append(name_surf)
                lead_list.append(score_surf)
                y_offset += 50

        self.leader_board = Menu(self, buttons=[menu_button2], text_surf=lead_list)
        for item in self.status.keys():
            if item == 'in_leaderboard':
                self.status[item] = True
            else:
                self.status[item] = False

    def update_leaderboard(self, new_elem: dict) -> None:  # Add new score to leaderboard
        self.leaderboard.append(new_elem)

    def set_fps(self) -> None:
        if self.fps == 30:
            self.fps = 60
        else:
            self.fps = 30
        self.main_menu.fps = self.fps

    def get_fps(self) -> int:
        return self.fps

    def set_music(self) -> None:
        self.game_music_on = abs(self.game_music_on - 1)
        self.music_status = self.STATUS[self.game_music_on]

    def get_music(self) -> str:
        return self.music_status

    def main(self) -> None:
        fps_clock = pygame.time.Clock()
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    running = False

            self.WINDOW.fill((0, 0, 0))

            for state, verif in self.status.items():
                if state == 'in_menu' and verif is True:
                    self.main_menu.update()
                    self.WINDOW.blit(self.title_img, self.title_rect)
                elif state == 'in_settings' and verif is True:
                    self.settings_menu.update()
                elif state == 'in_game' and verif is True:
                    if self.game.running:
                        self.game.update(events)
                    else:
                        self.go_menu()
                        if not self.game.awaiting_name and self.game.name != 'Admin023':
                            self.update_leaderboard(self.game.get_data())
                elif state == 'in_leaderboard' and verif is True:
                    self.leader_board.update()

            pygame.display.update()
            fps_clock.tick(self.fps)

        self.close_window()

    def close_window(self) -> None:
        with open('./data/leaderboard.json', 'w') as f:
            json.dump(self.leaderboard, f)

        pygame.quit()
        f.close()
        sys.exit(0)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    window = GameWindow()
    window.main()
