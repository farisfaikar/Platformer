import pygame
from os import walk


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_assets(path, ani_dict):
    sprite_path = path
    animations = ani_dict

    for animation in animations.keys():
        full_path = sprite_path + animation
        animations[animation] = import_folder(full_path)

    return animations
