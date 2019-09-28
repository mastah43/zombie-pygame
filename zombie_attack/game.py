import sys
import logging
import pygame.draw_py
from . import player
from . import animation
from . import zombie_group
from . import blood
from . import life
from .sfx import sfx


class ZombieAttackGame:
    COLOR_BACKGROUND = pygame.Color('black')

    @staticmethod
    def create_screen():
        screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption('Zombies Attack!!!')
        return screen

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self._play_music()

        self.screen = ZombieAttackGame.create_screen()
        self.font = pygame.font.SysFont('None', 19)

        screen_rect: pygame.sprite.Rect = self.screen.get_rect()
        player_pos_initial = (screen_rect.centerx, screen_rect.centery)
        self.player = player.Player(position=player_pos_initial, add_bullet=self.add_bullet)
        self.players = pygame.sprite.RenderPlain(self.player)
        self.bullets = pygame.sprite.RenderPlain()

        self.zombies = zombie_group.ZombieGroup(self._create_spawn_rects(screen_rect))
        self.effects = pygame.sprite.RenderPlain()

        blood.Blood.containers = self.effects
        life.ScoreIncrease.containers = self.effects

    def _create_spawn_rects(self, screen_rect):
        spawn_area_size = 100
        left = screen_rect.left - spawn_area_size
        top = screen_rect.top  # TODO - spawn_area_size
        width = screen_rect.width + spawn_area_size * 2
        height = spawn_area_size
        spawn_rect = pygame.sprite.Rect((left, top), (width, height))
        spawn_rects = [spawn_rect]
        # TODO continue
        return spawn_rects

    def _play_music(self):
        pygame.mixer.music.load("zombie_attack/music/random silly chip song.ogg")
        pygame.mixer.music.play(-1)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.trigger_weapon()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            self.player.turn_left()
        if keys_pressed[pygame.K_RIGHT]:
            self.player.turn_right()
        if keys_pressed[pygame.K_SPACE]:
            self.player.trigger_weapon()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self._clock_tick(clock)
            self._handle_input()
            self._update_model()
            self._draw_screen()

    def _clock_tick(self, clock):
        clock.tick(30)
        animation.update_delta_time(clock.get_time())

    def _update_model(self):
        self.players.update()
        self.bullets.update()
        self.zombies.update()
        self.effects.update()
        self._detect_bullet_hits()
        self._detect_zombie_attacks()

    def _draw_screen(self):
        self.screen.fill(ZombieAttackGame.COLOR_BACKGROUND)
        self.players.draw(self.screen)
        self.zombies.draw(self.screen)
        self.effects.draw(self.screen)
        self.bullets.draw(self.screen)
        self._draw_ui()
        pygame.display.flip()

    def _draw_ui(self):
        self._draw_player_state()

    def _detect_bullet_hits(self):
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.zombies, dokill=0)
            for hit in hits:
                logging.debug("bullet %s hit %s", bullet, hit)
                hit.hit(bullet.get_attack_points())
                bullet.kill()

    def _detect_zombie_attacks(self):
        hits = pygame.sprite.spritecollide(self.player, self.zombies, dokill=0)
        for hit in hits:
            # TODO make clear that hit is of Zombie type
            self.player.hit(hit.get_attack_points())
            if self.player.get_hit_points_amount() < 1:
                self.player.kill()
            logging.debug("zombie %s hit %s", hit, self.player)
            sfx.play_zombie_attack()
            sfx.play_player_hit()

    def _draw_player_state(self):
        # TODO use hearts instead?
        life = self.player.get_hit_points_amount()*100
        rendered = self.font.render('Life ' + str(life), 0, (255, 100, 100))
        self.screen.blit(rendered, (self.screen.get_size()[0] - 100, 0))  # TODO use pix width

