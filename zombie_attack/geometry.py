import pygame
from pygame.locals import *


def is_rect_outside_rect(rect_object: Rect, rect_area: Rect):
    return rect_object.bottom < rect_area.top \
           or rect_object.top > rect_area.bottom \
           or rect_object.left > rect_area.right \
           or rect_object.right < rect_area.left

