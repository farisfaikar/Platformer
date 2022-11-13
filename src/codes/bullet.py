import pygame
from src.codes.tools import import_folder


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size, direction):
        super().__init__()
        self.import_bullet_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += tile_size - self.image.get_size()[1]
        self.speed = 3 * direction

    def import_bullet_assets(self):
        bullet_path = 'src/sprites/bullet/'
        self.animations = {'run': []}

        for animation in self.animations.keys():
            full_path = bullet_path + animation
            self.animations[animation] = import_folder(full_path)

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
        # self.reverse_image()  # TODO: minor - figure out enemy flip

        self.rect.x += shift
