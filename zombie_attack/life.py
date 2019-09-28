import pygame
import logging
import sys
import typing
from . import identifiable

_log = logging.getLogger(__name__)


# TODO how to derive from Sprite so that kill method can be used without doubt
class Life:
    def __init__(self,
                 hit_points: float,
                 time_to_live: int = sys.maxsize - 1,
                 hit_point_regenerate_period: int = -1):
        self. _hit_points_max = hit_points
        self._hit_points = self._hit_points_max
        self._time_to_die = time_to_live + pygame.time.get_ticks()
        self._hit_point_regenerate_period = hit_point_regenerate_period
        self._hit_point_regenerate_time_start = pygame.time.get_ticks()

    def hit(self, attack_points: int):
        assert attack_points >= 0
        self._hit_points = max(self._hit_points - attack_points, 0)
        _log.debug(f"{self} got hit with {attack_points} now having {self._hit_points} hit points")
        if self._hit_points <= 0:
            self.die()

    def get_hit_points_amount(self) -> float:
        return self._hit_points/self._hit_points_max

    def die(self):
        _log.debug(f"{self} dies")
        self.kill()

    def update(self):
        self._die_after_timeout()
        self._regenerate_hit_points()

    def _get_time_to_live_left(self):
        return max(0, self._time_to_die - pygame.time.get_ticks())

    def _die_after_timeout(self):
        if self._get_time_to_live_left() <= 0:
            _log.debug(f"{self} will die after time to live passed")
            self.die()

    def _regenerate_hit_points(self):
        if self._hit_point_regenerate_period > 0 and self.get_hit_points_amount() > 0:
            time_regenerate_wait = pygame.time.get_ticks() - self._hit_point_regenerate_time_start
            time_regenerate_left: int = time_regenerate_wait - self._hit_point_regenerate_period
            if time_regenerate_left <= 0:
                self._hit_points = min(self._hit_points_max, self._hit_points + 1)
                self._hit_point_regenerate_time_start = pygame.time.get_ticks() + time_regenerate_left
                _log.debug(f"{self} regenerated hit point, time regenerate left {time_regenerate_left}")


class ScoreIncrease(pygame.sprite.Sprite, Life, identifiable.Identifiable):
    WIDTH = 100
    HEIGHT = 20
    TIME_TO_LIVE = 3000
    containers = None

    # TODO avoid redundancy in create_rect between classes by using mixin or utility
    @staticmethod
    def _create_rect(position: typing.Tuple[int, int], size: typing.Tuple[int, int]) -> pygame.sprite.Rect:
        x = position[0] - (size[0] / 2)
        y = position[1] - (size[1] / 2)
        return pygame.sprite.Rect((x, y), size)

    def __init__(self,
                 score_increase: int,
                 position: typing.Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self, self.containers)
        Life.__init__(self, hit_points=1, time_to_live=self.TIME_TO_LIVE)
        identifiable.Identifiable.__init__(self)
        self._score_increase = score_increase
        self.rect = self._create_rect(position, (self.WIDTH, self.HEIGHT))
        self.image = pygame.Surface(self.rect.size)
        self.image.set_colorkey(pygame.Color('black'))
        _log.debug(f"created {self} on {position}")

    def update(self, *args):
        Life.update(self)
        self._draw_image()
        # TODO enlarge font

    def _draw_image(self):
        self._draw_score_points()

    def _draw_score_points(self):
        font = pygame.font.SysFont('None', 19)  # TODO store font as constant field
        text = f"{round(self._score_increase)}"
        color = self._get_score_font_color()
        rendered = font.render(text, 0, color)
        self.image.blit(rendered, (50, 50))

    def _get_score_font_color(self):
        ttl_passed_amount = 1 - self._get_time_to_live_left() / float(self.TIME_TO_LIVE)
        color = (
            255 - 255 * ttl_passed_amount,
            100 - 100 * ttl_passed_amount,
            100 - ttl_passed_amount * 100)
        color = (255,255,255)
        return color

