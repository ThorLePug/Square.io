import pygame
from pygame.locals import *
from .entities.player import Player
from .entities.enemy import Enemy, EnemyShooter, SpiralShooter
from .walls import load_map, create_map
from ..utils.crosshair import Crosshair
from ..utils.animations import Fader
from ..utils.text_system import TextSurf


class Game:
    def __init__(self, window) -> None:
        self.software = window
        self.WINDOW = window.WINDOW
        self.delta_fps = 60/window.fps
        self.running = True
        self.awaiting_name = True
        self.changing_level = False
        self.fader = Fader()

        self.name_surf = TextSurf('NAME : ', window.title_font, self.WINDOW.get_width(), 300, anchor='left')

        # Score
        self.score = 0
        self.wave = 0
        self.name = ''

        self.game_music = pygame.mixer.Sound('sound/game_music.wav')
        self.level_up = pygame.mixer.Sound('sound/level_up.wav')
        self.player_hit = pygame.mixer.Sound('sound/player_hit.wav')
        self.shooting = pygame.mixer.Sound('sound/shooting.wav')
        self.game_over_img = pygame.image.load('img/game_over.png')

        self.press_k_surf = TextSurf('Press SPACE to continue', self.software.text_font, 640, 480)
        self.score_surf = None

        # Map Making
        map1_data = load_map()
        self.map1_objects = create_map(map1_data)
        self.walls = []
        for row in self.map1_objects:
            for block in row:
                if block.type == 'wall':
                    self.walls.append(pygame.Rect(block.x, block.y, block.width, block.height))

        self.P1 = Player(self.WINDOW, self.delta_fps)
        self.all_bullets = pygame.sprite.Group()
        self.all_bullets.add(self.P1.bullets)

        self.all_sprite_group = pygame.sprite.Group()
        self.all_sprite_group.add(self.P1)

        self.mouse_x = 0
        self.mouse_y = 0

        self.enemy_num = 0
        self.enemy_shooter_targeting_num = -4
        self.spiral_enemy_shooter_num = -3
        self.enemy_group = pygame.sprite.Group()
        self.shooting_enemies = pygame.sprite.Group()
        self.shooting_targeting_enemies = pygame.sprite.Group()
        self.non_targeting_enemies = pygame.sprite.Group()

        self.crosshair = Crosshair()
        self.crosshair_group = pygame.sprite.GroupSingle(self.crosshair)

        self.enemy_setup()

    def enemy_setup(self) -> None:

        for x in range(self.enemy_num):
            enemy = Enemy(self.WINDOW.get_width(), self.WINDOW.get_height(), self.all_sprite_group, self.walls,
                          self.WINDOW, self.delta_fps)
            self.enemy_group.add(enemy)
            self.all_sprite_group.add(enemy)

        for y in range(self.enemy_shooter_targeting_num):
            enemy_shooter = EnemyShooter(self.WINDOW.get_width(), self.WINDOW.get_height(), self.all_sprite_group,
                                         self.walls, self.WINDOW, self.delta_fps)
            self.enemy_group.add(enemy_shooter)
            self.all_sprite_group.add(enemy_shooter)
            self.shooting_targeting_enemies.add(enemy_shooter)

            self.shooting_enemies.add(enemy_shooter)
            self.all_bullets.add()

        for z in range(self.spiral_enemy_shooter_num):
            spiral_enemy_shooter = \
                SpiralShooter(self.WINDOW.get_width(), self.WINDOW.get_height(), self.all_sprite_group, self.walls,
                              self.WINDOW, self.delta_fps)
            self.enemy_group.add(spiral_enemy_shooter)
            self.all_sprite_group.add(spiral_enemy_shooter)
            self.non_targeting_enemies.add(spiral_enemy_shooter)

            self.shooting_enemies.add(spiral_enemy_shooter)
        self.enemy_num += 1
        self.enemy_shooter_targeting_num += 1
        self.spiral_enemy_shooter_num += 1

    def handle_input(self) -> None:
        k_pressed = pygame.key.get_pressed()

        if not self.P1.is_killed:
            # Keyboard input
            '''
            for character in CHARACTERS:
                if k_pressed[pygame.key.key_code(character)]:
                    print(character)
            '''
            if k_pressed[K_RIGHT]:
                self.P1.move('right', self.P1.speed)
            elif k_pressed[K_LEFT]:
                self.P1.move('left', self.P1.speed)
            elif k_pressed[K_DOWN]:
                self.P1.move('down', self.P1.speed)
            elif k_pressed[K_UP]:
                self.P1.move('up', self.P1.speed)

            if k_pressed[K_SPACE]:
                self.P1.get_shield()

            # Mouse Input
            mouse_click = pygame.mouse.get_pressed(num_buttons=3)

            if mouse_click[0]:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                self.P1.shoot(self.P1.position, self.mouse_x, self.mouse_y, self.WINDOW)

        elif self.fader.alpha >= 255:   # Way to check if 0.5 sec has passed to avoid straight menu bar
            if k_pressed[K_SPACE]:
                self.running = False

    def await_name(self, events):
        text = self.name_surf.text_in
        for event in events:
            if event.type == KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(text) >= 8:
                        text = text[:-1]
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    self.name = text[7:]
                    self.awaiting_name = False
                    if self.software.game_music_on:
                        self.game_music.play(loops=-1)
                else:
                    if len(text) - 6 <= 15:
                        text += event.unicode
        self.name_surf.text_in = text
        try:
            self.name_surf.draw(self.WINDOW)
        except KeyError:
            self.name_surf.text_in = self.name_surf.text_in[:-1]

    def enemy_control(self) -> None:
        if not self.P1.is_killed:
            for enemy in self.shooting_targeting_enemies.sprites():
                enemy.shoot(enemy.position, self.P1.position[0], self.P1.position[1], self.WINDOW)
            for enemy in self.non_targeting_enemies.sprites():
                enemy.shoot(enemy.position, enemy.target_x, enemy.target_y, self.WINDOW)

    def check_collision(self) -> None:
        for enemy in self.enemy_group.sprites():
            collided = enemy.rect.collidelist(self.P1.bullets)
            if collided > -1 and not enemy.is_killed:
                enemy.health -= 30
                if enemy.health <= 0:
                    enemy.is_killed = True
                    self.score += 1
                self.P1.bullets.pop(collided)

        # Bullets kill Player
        for enemy in self.shooting_enemies.sprites():
            collided = self.P1.rect.collidelist(enemy.bullets)
            if collided > -1:
                self.P1.health -= 30
                self.player_hit.play()
                enemy.bullets.pop(collided)
                if self.P1.health <= 0:
                    self.P1.is_killed = True
                    self.P1.disappear()
            if self.P1.has_shield:
                for bullet in enemy.bullets:
                    if pygame.sprite.collide_circle(self.P1.shield, bullet):
                        enemy.bullets.remove(bullet)
            for bullet in enemy.bullets:
                if bullet.rect.collidelist(self.walls) > -1:
                    enemy.bullets.remove(bullet)

        # Enemy/Bullet kills player
        if pygame.sprite.spritecollideany(self.P1, self.enemy_group):
            self.player_hit.play()
            self.P1.is_killed = True

        if self.P1.rect.collidelist(self.walls) > -1:
            self.P1.move_back()

        for bullet in self.P1.bullets:
            if bullet.rect.collidelist(self.walls) > -1:
                self.P1.bullets.remove(bullet)

    def check_next_wave(self) -> None:
        if self.all_sprite_group.has(self.P1) and len(self.all_sprite_group.sprites()) == 1:
            self.enemy_setup()

            """
            boss = BossMonster(self.WINDOW.get_width(), self.WINDOW.get_height(), self.all_sprite_group, self.walls,
                               self.WINDOW, self.delta_fps)
            self.all_sprite_group.add(boss)
            """
            self.wave += 1
            self.level_up.play(loops=0)

        if self.P1.is_killed:
            self.changing_level = True
            self.score_surf = TextSurf(f'SCORE : {self.score}', self.software.title_font, 640, 390)
            self.game_music.fadeout(100)

    def update(self, events) -> None:
        if self.awaiting_name:
            self.await_name(events)
        else:
            self.P1.save_position()

            self.WINDOW.fill((0, 0, 0))

            # Handle input
            self.handle_input()

            # Control enemy movement + shooting
            self.enemy_control()

            # Update + collision detection
            # if not self.changing_level:

            self.all_sprite_group.update()
            self.check_collision()
            self.P1.power_up.draw(self.WINDOW)

            # Handle Rendering
            self.all_sprite_group.draw(self.WINDOW)

            for row in self.map1_objects:
                for block in row:
                    block.render(self.WINDOW)

            if not self.P1.is_killed:
                health_bar_rect = pygame.Rect(0, 0, 70, 7)
                health_bar_rect.center = (self.P1.rect.centerx, self.P1.rect.centery - 50)
                pygame.draw.rect(self.WINDOW, (150, 150, 150), health_bar_rect)
                width = (self.P1.health / self.P1.total_health) * 70
                health_rect = pygame.Rect(health_bar_rect.left, health_bar_rect.top, width, 7)
                pygame.draw.rect(self.WINDOW, (0, 255, 0), health_rect)

            self.software.text_font.render(self.WINDOW, f'SCORE: {self.score}', (20, 20))
            self.software.text_font.render(self.WINDOW, f'WAVE: {self.wave}', (self.WINDOW.get_width() - 70, 20))
            self.check_next_wave()

            if self.changing_level:
                if self.fader.alpha <= 255:
                    self.fader.fade(self.WINDOW)
                else:
                    self.WINDOW.fill((0, 0, 0))
                    self.WINDOW.blit(self.game_over_img, (70, 200))
                    self.press_k_surf.draw(self.WINDOW)
                    self.score_surf.draw(self.WINDOW)

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        self.crosshair_group.update(mouse_pos_x, mouse_pos_y)
        self.crosshair_group.draw(self.WINDOW)

    def get_data(self):
        data_dict = {'Name': self.name, 'Score': self.score}
        return data_dict
