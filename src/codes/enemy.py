import pygame
from src.codes.tools import import_assets


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        self.animations = import_assets('src/sprites/enemy/', {'run': []})
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += tile_size - self.image.get_size()[1]
        self.speed = 1

    def animate(self):
        animation = self.animations['run']

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.animate()
        self.move()
        self.reverse_image()

        self.rect.x += shift
