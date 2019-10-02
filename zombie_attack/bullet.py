import pygame
import logging
from . import animation
from . import identifiable
from . import life
from .gfx import gfx


_log = logging.getLogger(__name__)


class Bullet(pygame.sprite.Sprite, identifiable.Identifiable, life.Life):
    TIME_TO_LIVE = 1000
    containers = None

    def __init__(self, position, direction, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        identifiable.Identifiable.__init__(self)
        life.Life.__init__(self, hit_points=1, time_to_live=self.TIME_TO_LIVE)
        self.direction = direction
        self.speed = speed
        self.image = gfx.get_image_bullet()
        self.rect = pygame.sprite.Rect(self.image.get_rect())
        self.rect.move_ip((position[0] - self.rect.width/2,
                           position[1] - self.rect.height/2))
        self.time_created = pygame.time.get_ticks()
        _log.debug(f"{self} created with direction {self.direction} and speed {self.speed}")

    def update(self, *args):
        life.Life.update(self)
        self._move_in_shot_direction()

    def _move_in_shot_direction(self):
        distances_delta = animation.value_sec_by_delta_time(self.speed)
        self.rect.move_ip(self.direction[0] * distances_delta, self.direction[1] * distances_delta)

    def get_attack_points(self):
        return 5.


class Slash(Bullet):

    def __init__(self, target_position):
        Bullet.__init(position=target_position, direction=(0, 0), speed=0)
        self.image = None  # TODO add animated visualization of slash


