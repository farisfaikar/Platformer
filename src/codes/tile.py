import pygame
from src.codes.tools import import_assets


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        self.animations = import_assets('src/sprites/tile/', {'idle': []})
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):
        animation = self.animations['idle']

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
