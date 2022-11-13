import pygame
from src.codes.tools import import_folder


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        self.import_enemy_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += tile_size - self.image.get_size()[1]
        self.speed = 1

    def import_enemy_assets(self):
        enemy_path = 'src/sprites/enemy/'
        self.animations = {'run': []}

        for animation in self.animations.keys():
            full_path = enemy_path + animation
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


class Shooter(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        self.import_shooter_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # shooter attribute
        self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.y += tile_size - self.image.get_size()[1]
        self.speed = 1

        # bullet attribute
        self.bullet_image = self.animations['bullet'][self.frame_index]
        self.bullet_rect = self.bullet_image.get_rect(topleft=pos)
        self.bullet_rect.y += tile_size - self.bullet_image.get_size()[1]
        self.bullet_speed = 2

    def import_shooter_assets(self):
        shooter_path = 'src/sprites/shooter/'
        self.animations = {'run': [], 'bullet': []}

        for animation in self.animations.keys():
            full_path = shooter_path + animation
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

    def move_bullet(self):
        self.bullet_rect.x += self.bullet_speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def animate_bullet(self):
        animation = self.animations['bullet']

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.bullet_image = animation[int(self.frame_index)]
        self.bullet_rect = self.bullet_image.get_rect(midbottom=self.bullet_rect.midbottom)

    def update(self, shift):
        # shooter methods
        self.animate()
        self.move()

        # bullet methods
        # self.animate_bullet()
        # self.move_bullet()
        # self.reverse_image()  # TODO: minor - figure out enemy flip

        self.rect.x += shift
