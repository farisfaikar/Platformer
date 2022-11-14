import pygame
from src.codes.tools import import_folder


class Finish(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        self.import_finish_assets()
        self.frame_index = 0
        self.animation_speed = 0.05
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += tile_size - self.image.get_size()[1]

    def import_finish_assets(self):
        tile_path = 'src/sprites/finish/'
        self.animations = {'idle': []}

        for animation in self.animations.keys():
            full_path = tile_path + animation
            self.animations[animation] = import_folder(full_path)

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
