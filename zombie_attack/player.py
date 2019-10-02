import pygame
import math
import logging
import typing
from . import weapon
from . import animation
from . import life
from .gfx import gfx


_log = logging.getLogger(__name__)


class Player(pygame.sprite.Sprite, life.Life):
    ROTATION_IMAGE = 0  # soldier is facing top but 0 degrees is facing right
    WEAPON_OUT_DISTANCE_FROM_CENTER = 64
    HIT_POINTS_INITIAL = 100
    HIT_POINTS_REGENERATE_PERIOD = 500

    @staticmethod
    def _create_rect(position: typing.Tuple[int, int], size: int) -> pygame.sprite.Rect:
        x = position[0] - (size / 2)
        y = position[1] - (size / 2)
        rect = pygame.sprite.Rect((x, y), (size, size))
        return rect

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        life.Life.__init__(self, self.HIT_POINTS_INITIAL,
                           hit_point_regenerate_period=self.HIT_POINTS_REGENERATE_PERIOD)

        self.rect = self._create_rect(position, 128)
        self.image = pygame.Surface(self.rect.size)
        _log.debug("created player on position {position}")
        self._rotation_degrees = 0
        self._weapon = weapon.Weapon()
        self._turn_degrees_per_sec = 360

    def update(self, *args):
        life.Life.update(self)
        self._weapon.update()
        self._draw()

    def trigger_weapon(self):
        self._weapon.trigger()
        return

    def turn_left(self):
        self._turn(self._get_turn_degrees_by_delta_time())

    def turn_right(self):
        self._turn(-self._get_turn_degrees_by_delta_time())

    def _turn(self, rotation_diff):
        self._rotation_degrees = (self._rotation_degrees + rotation_diff) % 360
        _log.debug("player turns to %d degrees pointing to %s", self._rotation_degrees, self._get_direction())
        # TODO self.rect = self.image.get_rect(center=self.rect.center)  # TODO why rotate image and rect?
        self._update_weapon_position_and_direction()

    def _draw(self):
        self._draw_soldier()
        self._draw_boundary()
        self._draw_line_fire_direction()

    def _draw_soldier(self):
        image_org = gfx.get_image_player()
        _log.debug(f"scaling {self} to {self.rect.size}" +
                   f" onto image sized {image_org.get_rect().size}")
        scale = self.rect.width / image_org.get_rect().width
        rotation_image = (self._rotation_degrees - self.ROTATION_IMAGE) % 360
        _log.debug(
            f"{self} rotation {self._rotation_degrees} and image {rotation_image}" +
            f" using const {self.ROTATION_IMAGE}")
        self.image = pygame.transform.rotozoom(image_org, rotation_image, scale)
        self.image.set_colorkey(pygame.Color('black'))

    def _draw_line_fire_direction(self):
        direction = self._get_direction()
        pygame.draw.line(
            self.image,
            pygame.Color('red'),
            self.image.get_rect().center,
            (
                self.image.get_rect().centerx + (direction[0] * 100),
                self.image.get_rect().centery + (direction[1] * 100)
            ))

    def _draw_boundary(self):
        pygame.draw.rect(
            self.image,
            pygame.Color('blue'),
            self.image.get_rect(),
            1)

    def _update_weapon_position_and_direction(self):
        weapon_direction = self._get_direction()
        weapon_out_pos_abs = tuple(p + (Player.WEAPON_OUT_DISTANCE_FROM_CENTER * d)
                                   for p, d in zip(self.rect.center, weapon_direction))
        _log.debug("weapon pos abs %s", weapon_out_pos_abs)
        self._weapon.set_position_and_direction(weapon_out_pos_abs, weapon_direction)

    def _get_direction(self):
        rotation_radians = math.radians(self._rotation_degrees)
        direction_x = -math.sin(rotation_radians)
        direction_y = -math.cos(rotation_radians)
        return direction_x, direction_y

    def _get_turn_degrees_by_delta_time(self):
        return animation.value_sec_by_delta_time(self._turn_degrees_per_sec)







