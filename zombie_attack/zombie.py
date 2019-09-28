import pygame
import logging
import math
import random
import typing
from .gfx import gfx
from . import animation
from . import life
from . import identifiable
from . import blood

_random = random.Random()
_log = logging.getLogger(__name__)


class Zombie(pygame.sprite.Sprite, life.Life, identifiable.Identifiable):
    ROTATION_IMAGE = 0  # zombie is facing right in images
    HIT_POINTS = 10
    TIME_TO_LIVE = 10000000  # TODO 10000
    SCORE = 50

    @staticmethod
    def _create_rect(position: typing.Tuple[int, int], size: int) -> pygame.sprite.Rect:
        x = position[0] - (size / 2)
        y = position[1] - (size / 2)
        rect = pygame.sprite.Rect((x, y), (size, size))
        return rect

    def __init__(self,
                 position: typing.Tuple[int, int],
                 size: int,
                 rotation: int,
                 target_position: typing.Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        life.Life.__init__(self, self.HIT_POINTS, self.TIME_TO_LIVE)
        identifiable.Identifiable.__init__(self)
        self._turn_degrees_per_sec = 45
        self._move_distance_per_sec = 50
        self._animation_frame = 0
        self.target_position = target_position
        _log.debug("created %s on position %s sized %s with rotation %s", self, position, size, rotation)
        self._rotation_degrees = rotation
        self._score = self.SCORE
        # TODO let zombie idle after a while when he heard no sounds
        # TODO show sound circle animation so that it is clear that zombie heard sound
        # TODO let zombie be in idle state for a while
        # TODO let zombie attack when in proximity of target

        self.rect = self._create_rect(position, size)
        self.image = pygame.Surface(self.rect.size)
        _log.debug("created %s image buffer with size %s", self, self.image.get_rect().size)

    def _move(self, xy_delta: typing.Tuple[int, int]):
        self._animation_frame += 1
        self.rect.move_ip(xy_delta[0], xy_delta[1])
        _log.debug(f"{self} moved by {xy_delta} ")

    def _draw(self):
        image_org = gfx.get_image_zombie_move(self._animation_frame)
        _log.debug(f"scaling {self} to {self.rect.size}" +
                   f" onto image sized {image_org.get_rect().size}")
        scale = self.rect.width / image_org.get_rect().width
        rotation_image = (self._rotation_degrees - Zombie.ROTATION_IMAGE) % 360
        _log.debug(
            f"{self} rotation {self._rotation_degrees} and image {rotation_image}" +
            f" using const {self.ROTATION_IMAGE}")
        self.image = pygame.transform.rotozoom(image_org, rotation_image, scale)
        self.image.set_colorkey(pygame.Color('black'))

        self._draw_rotation_degrees()
        self._draw_boundary()

        # TODO why does render_to not exist?
        #font.render_to(surf=self.image, dest=self.image, text=text,
        #               fgcolor=0, bgcolor=(255, 100, 100))

    def _draw_rotation_degrees(self):
        font = pygame.font.SysFont('None', 19)
        text = f"{round(self._rotation_degrees)}"
        rendered = font.render(text, 0, (255, 100, 100))
        self.image.blit(rendered, (50, 50))

    def _draw_boundary(self):
        pygame.draw.rect(
            self.image,
            pygame.Color('blue'),
            self.image.get_rect(),
            1)

    def update(self, *args):
        life.Life.update(self)
        self._move_to_target()

    def _move_to_target(self):
        draw_funcs = []

        tx = self.target_position[0]
        ty = self.target_position[1]
        dx = tx - self.rect.centerx
        dy = ty - self.rect.centery

        def draw_line_target_direction():
            rect = self.image.get_rect()
            pygame.draw.line(
                self.image,
                pygame.Color('white'),
                rect.center,
                (
                    rect.centerx + (dx * 50),
                    rect.centery + (dy * 50)
                ))

        draw_funcs.append(draw_line_target_direction)

        rotation_facing_target = int(math.atan2(dy, dx)/math.pi*180)
        rotation_delta = rotation_facing_target - self._rotation_degrees
        if rotation_delta != 0:
            rotation_direction = 1 if 0 < rotation_delta <= 180 else -1
            rotation_delta_step = animation.value_sec_by_delta_time(self._turn_degrees_per_sec)*rotation_direction
            _log.debug(f"{self} with rotation {self._rotation_degrees}" +
                       f" turning by {rotation_delta_step} in direction {rotation_facing_target}")
            # TODO make turn angle stop at facing target
            self._rotation_degrees = (self._rotation_degrees + rotation_delta_step) % 360

        distance = math.sqrt((dx * dx) + (dy * dy))

        if distance > 0:
            rotation_radians = (self._rotation_degrees/180.)*math.pi
            mx = math.cos(rotation_radians)
            my = math.sin(rotation_radians)
            _log.debug(f"{self} heading in direction {mx}, {my}")

            def draw_line_move_direction():
                pygame.draw.line(
                    self.image,
                    pygame.Color('green'),
                    self.image.get_rect().center,
                    (
                        self.image.get_rect().centerx + (mx * 60),
                        self.image.get_rect().centery + (my * 60)
                    ))

            draw_funcs.append(draw_line_move_direction)

            m_length = math.sqrt((mx * mx) + (my * my))
            if m_length > 0:
                mx_normalized = mx / m_length
                my_normalized = my / m_length
                distance_delta = animation.value_sec_by_delta_time(self._move_distance_per_sec)
                self._move((mx_normalized * distance_delta, my_normalized * distance_delta))

        self._draw()

        for draw_func in draw_funcs:
            draw_func()

    def _get_turn_degrees_by_delta_time(self):
        return animation.value_sec_by_delta_time(self._turn_degrees_per_sec)

    def get_attack_points(self):
        return 20

    def die(self):
        super(Zombie, self).die()
        self._add_blood_effect()
        self._add_score_effect()

    def _add_blood_effect(self):
        blood.Blood(self.rect.center, 50)

    def _add_score_effect(self):
        position = (self.rect.centerx, self.rect.centery + 200)
        life.ScoreIncrease(self._score, position)

