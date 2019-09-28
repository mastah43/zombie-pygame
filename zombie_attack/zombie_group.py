import pygame
import logging
import random
import typing
from . import zombie
from .sfx import sfx

_log = logging.getLogger(__name__)


class ZombieGroup(pygame.sprite.Group):
    SPAWN_PERIOD_INITIAL = 1500
    SPAWN_PERIOD_MIN = 500
    SPAWN_PERIOD_DECREASE = 50
    SPAWN_DELAY_INITIAL = -SPAWN_PERIOD_INITIAL
    ZOMBIE_SIZE_MEAN = 100

    def __init__(self, spawn_areas: typing.List[pygame.sprite.Rect]):
        pygame.sprite.Group.__init__(self)
        self.max_zombies = 1  # TODO 10
        self._spawn_areas = spawn_areas
        self._spawn_period = ZombieGroup.SPAWN_PERIOD_INITIAL
        self._spawn_time_start = pygame.time.get_ticks() + ZombieGroup.SPAWN_DELAY_INITIAL
        self._random = random.Random()
        pass

    def update(self, *args):
        super().update(args)
        self._spawn_zombie_on_timeout()

    def _spawn_zombie_on_timeout(self):
        if self._is_spawn_slot_available() and self._is_spawn_time_out():
            self._spawn_zombie()
            self._spawn_time_start = pygame.time.get_ticks()
            self._decrease_spawn_period()

    def _decrease_spawn_period(self):
        self._spawn_period -= ZombieGroup.SPAWN_PERIOD_DECREASE
        self._spawn_period = max(self._spawn_period, ZombieGroup.SPAWN_PERIOD_MIN)

    def _spawn_zombie(self):
        x, y = self._get_spawn_position_random()
        size_factor = 1. + random.normalvariate(0, 0.1)
        rotation = random.randint(0, 359)
        size = ZombieGroup.ZOMBIE_SIZE_MEAN*size_factor
        target_position = (400, 300)  # TODO get dynamically pos of player nvia listening to bullet shot events
        _zombie = zombie.Zombie((x, y), size, rotation, target_position)
        self.add(_zombie)
        sfx.play_zombie_spawn()
        _log.debug("added zombie %d", _zombie.id)

    def _get_spawn_position_random(self):
        spawn_area = self._random.choice(self._spawn_areas)
        return self._get_spawn_position_random_single_area(spawn_area)

    def _get_spawn_position_random_single_area(self, spawn_area):
        x = self._random.randint(spawn_area.left, spawn_area.right)
        y = self._random.randint(spawn_area.top, spawn_area.bottom)
        return x, y

    def _is_spawn_time_out(self):
        return pygame.time.get_ticks() - self._spawn_time_start >= self._spawn_period

    def _is_spawn_slot_available(self):
        return len(self.sprites()) < self.max_zombies
