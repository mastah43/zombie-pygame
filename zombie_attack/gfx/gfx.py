import pygame
import os
import random
import logging

_gfx_library = {}
_random = random.Random()


def get_image_zombie_move(step: int) -> pygame.Surface:
    frame = step % 17
    path = f"zombie/skeleton-move_{frame}.png"
    return _get_image(path)


def get_image_blood(step: int) -> pygame.Surface:
    frame = step % 15
    path = f"blood/bloodsplat3_strip15.png"
    image_sheet = _get_image(path)
    # TODO optimize: find better way to have image once in memory

    width = 480
    height = width
    size = [width, height]
    x = width*frame
    y = 0

    image = pygame.Surface(size).convert()
    image.blit(image_sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(pygame.Color("black"))

    return image


def get_image_player() -> pygame.Surface:
    return _get_image("soldier/player.png")


def get_image_bullet() -> pygame.Surface:
    return _get_image("bullet/bullet.png")


def _get_image(path_below_gfx) -> pygame.Surface:
    global _gfx_library
    path = "zombie_attack/gfx/" + path_below_gfx
    image = _gfx_library.get(path)
    if image is None:
        path_os = path.replace('/', os.sep).replace('\\', os.sep)
        try:
            image = pygame.image.load(path_os)
        except pygame.error:
            raise ValueError('Cannot load image: ' + path_os)

        image = image.convert_alpha()
        _gfx_library[path] = image

    return image


