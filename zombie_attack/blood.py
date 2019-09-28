import pygame
import logging
import math
import random
import typing
from .gfx import gfx
from . import animation
from . import identifiable
from .sfx import sfx

_random = random.Random()
_log = logging.Logger(__name__, level=logging.DEBUG)


class Blood(pygame.sprite.Sprite, animation.AnimationTimed, identifiable.Identifiable):
    ANIMATION_STEPS = 10
    containers = None

    # TODO avoid redundancy in create_rect between classes by using mixin or utility
    @staticmethod
    def _create_rect(position: typing.Tuple[int, int], size: int) -> pygame.sprite.Rect:
        x = position[0] - (size / 2)
        y = position[1] - (size / 2)
        return pygame.sprite.Rect((x, y), (size, size))

    def __init__(self,
                 position: typing.Tuple[int, int],
                 size: int):
        pygame.sprite.Sprite.__init__(self, self.containers)
        animation.AnimationTimed.__init__(self, steps_total=15, step_time_period=100)
        identifiable.Identifiable.__init__(self)
        self.rect = self._create_rect(position, size)
        self.image = pygame.Surface(self.rect.size)
        self.image.set_colorkey(pygame.Color('black'))
        self._update_image()
        _log.debug(f"created {self} on {position} sized {size}", position, size)
        sfx.play_zombie_die()

    def _update_image(self):
        image_org = gfx.get_image_blood(self._get_animation_step())
        pygame.transform.scale(image_org, self.rect.size, self.image)

    def update(self, *args):
        self._update_image()
        if self._is_animation_finished:
            self.kill()

