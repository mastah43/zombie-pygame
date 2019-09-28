import unittest
import pygame
import sys
from . import zombie
from . import animation


class ZombieTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

    def test_time_to_live(self):
        pass

    def test_move_to_target(self):
        z = zombie.Zombie(position=(0, 0), size=100, rotation=0, target_position=(100, 0))
        animation.update_delta_time(100)
        z.update()
        self.assertGreater(z.rect.x, -50)
        self.assertEquals(z.rect.y, 0)


if __name__ == '__main__':
    unittest.main()

