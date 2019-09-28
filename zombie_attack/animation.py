import pygame
import logging

_log = logging.Logger(__name__, level=logging.DEBUG)


def time_to_secs(time: float):
    return time / 1000.


def value_sec_by_time_millis(value_per_sec: float, time_ms: float):
    return time_to_secs(time_ms) * value_per_sec


def value_sec_by_delta_time(value_per_sec: float):
    return value_sec_by_time_millis(value_per_sec, get_delta_time_ms())


# having this globally is bad design - store in game instance and pass to update method of sprites
_delta_time_ms = -1


def update_delta_time(delta_time_ms):
    global _delta_time_ms
    _delta_time_ms = delta_time_ms


def get_delta_time_ms():
    return _delta_time_ms


class AnimationTimed:
    def __init__(self, steps_total: int, step_time_period: int, repeat=False):
        self._animation_timed_steps_total = steps_total
        self._animation_timed_repeat = repeat
        self._animation_timed_period = step_time_period
        self._animation_timed_start = pygame.time.get_ticks()

    def _get_animation_step(self):
        time = pygame.time.get_ticks()
        time_passed = time - self._animation_timed_start
        step = time_passed / self._animation_timed_period
        _log.debug(f"animation step {step} after {time_passed} ms" +
                   f" calculated from {time} - {self._animation_timed_start}")
        if self._animation_timed_repeat:
            return step % self._animation_timed_steps_total
        else:
            return min(step, self._animation_timed_steps_total - 1)

    def _is_animation_finished(self):
        return not self._animation_timed_repeat \
               and self._get_animation_step() >= self._animation_timed_steps_total - 1
