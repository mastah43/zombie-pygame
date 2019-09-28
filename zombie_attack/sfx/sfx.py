import pygame
import os
import random

_sound_library = {}
_random = random.Random()


def play_shot_pistol():
    file_name = _random.choice(("pistol", "pistol2", "pistol3"))
    _play_sound("shots/" + file_name + ".ogg")


def play_zombie_spawn():
    _play_sound("zombie/Zombie Sound.wav")


def play_zombie_attack():
    _play_sound("zombie/Zombie Attack Sound.wav")


def play_zombie_die():
    file_name = _random.choice(("impactsplat01", "impactsplat04", "impactsplat05", "impactsplat06"))
    _play_sound("splatter/" + file_name + ".mp3.flac")


def play_player_hit():
    _play_sound("aww/aw0" + str(_random.randint(1, 6)) + ".ogg")


def _play_sound(path_below_sfx):
    global _sound_library
    path = "zombie_attack/sfx/" + path_below_sfx
    sound = _sound_library.get(path)
    if sound is None:
        path_os = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(path_os)
        _sound_library[path] = sound
    sound.play()


