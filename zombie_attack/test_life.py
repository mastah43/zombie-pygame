import unittest
import pygame
import sys
pygame.init()
from . import life


class LifeTestable(life.Life):
    def __init__(self,
                 hit_points: float = 100,
                 time_to_live: int = sys.maxsize - 1,
                 hit_point_regenerate_period: int = -1):
        life.Life.__init__(self,
                           hit_points=hit_points,
                           time_to_live=time_to_live,
                           hit_point_regenerate_period=hit_point_regenerate_period)
        self.alive = True
        self.rect = pygame.sprite.Rect(0, 0, 10, 10)

    def kill(self):
        self.alive = False


class LifeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    def test_time_to_live(self):
        pass

    def test_hit(self):
        t = LifeTestable(hit_points=100)
        self._assert_hit_point_amount(t, 1)
        t.hit(50)
        self._assert_hit_point_amount(t, 0.5)

    def test_hit_kill_slowly(self):
        t = LifeTestable(hit_points=100)
        t.hit(50)
        t.hit(50)
        self._assert_hit_point_amount(t, 0)

    def test_hit_kill_single_exact_blow(self):
        t = LifeTestable(hit_points=100)
        t.hit(100)
        self._assert_hit_point_amount(t, 0)

    def test_hit_kill_single_super_blow(self):
        t = LifeTestable(hit_points=100)
        t.hit(200)
        self._assert_hit_point_amount(t, 0)

    def test_regenerate_hit_points(self):
        t = LifeTestable(hit_points=100, hit_point_regenerate_period=100)
        t.hit(10)
        self._assert_hit_point_amount(t, 0.9)
        pygame.time.delay(100)
        t.update()
        self._assert_hit_point_amount(t, 0.91)

    def test_regenerate_hit_points_not_after_death(self):
        t = LifeTestable(hit_points=100, hit_point_regenerate_period=100)
        t.hit(100)
        pygame.time.delay(100)
        t.update()
        self._assert_hit_point_amount(t, 0)

    def test_die_after_timeout(self):
        t = LifeTestable(hit_points=100, time_to_live=100)
        t.hit(100)
        pygame.time.delay(100)
        self._assert_hit_point_amount(t, 0)
        self.assertFalse(t.alive)

    def _assert_hit_point_amount(self, t, amount_expected):
        self.assertEqual(t.get_hit_points_amount(), amount_expected)


if __name__ == '__main__':
    unittest.main()

