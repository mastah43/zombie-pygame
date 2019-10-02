import pygame
import logging
from . import bullet
from . import animation
from .sfx import sfx

_log = logging.getLogger(__name__)


class Weapon(pygame.sprite.Sprite):
    RELOAD_PROGRESS_PER_SEC = 10
    BULLET_SPEED = 600

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.reload_progress = 1.
        self.rect = pygame.Rect((0, 0), (1, 1))
        self.direction = (0, 1)

    def update(self):
        reload_progress_before = self.reload_progress
        self.reload_progress = \
            min(1.,
                self.reload_progress
                + animation.value_sec_by_delta_time(Weapon.RELOAD_PROGRESS_PER_SEC))
        if reload_progress_before < 1 <= self.reload_progress:
            _log.debug("weapon is reloaded")

    def set_position_and_direction(self, position, direction):
        self.rect.move_ip(
            position[0] - self.rect.left,
            position[1] - self.rect.top)  # TODO improve
        self.direction = direction
        _log.debug(f"weapon at {self.rect.center} pointing to {self.direction}")

    def trigger(self):
        if self.reload_progress >= 1:
            _log.debug("weapon fires")
            sfx.play_shot_pistol()
            bullet.Bullet(
                position=self.rect.center,
                direction=self.direction,
                speed=self.BULLET_SPEED)
            self.reload_progress = 0
        else:
            _log.debug("weapon not reloaded - cannot fire")


