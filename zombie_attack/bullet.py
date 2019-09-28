import pygame
import logging
from . import animation
from . import identifiable
from .gfx import gfx


_log = logging.getLogger(__name__)


class Bullet(pygame.sprite.Sprite, identifiable.Identifiable):
    TIME_TO_LIVE = 1000

    def __init__(self, position, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        identifiable.Identifiable.__init__(self)
        self.direction = direction
        self.speed = speed
        self.image = gfx.get_image_bullet()
        self.rect = pygame.sprite.Rect(self.image.get_rect())
        self.rect.move_ip((position[0] - self.rect.width/2,
                           position[1] - self.rect.height/2))
        self.time_created = pygame.time.get_ticks()
        _log.debug(f"{self} created with direction {self.direction} and speed {self.speed}")

    def update(self, *args):
        self.move_in_shot_direction()
        self.kill_if_timeout()

    def move_in_shot_direction(self):
        distances_delta = animation.value_sec_by_delta_time(self.speed)
        self.rect = self.rect.move(self.direction[0] * distances_delta, self.direction[1] * distances_delta)

    def kill_if_timeout(self):
        if pygame.time.get_ticks() - self.time_created > Bullet.TIME_TO_LIVE:
            _log.debug(f"{self} killed after timeout")
            self.kill()

    def get_attack_points(self):
        return 5.



