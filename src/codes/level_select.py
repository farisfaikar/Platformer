import pygame
import src.codes.config as conf


class LevelSelect:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(conf.chary_font, 20)

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return 'exit'
            elif keys[pygame.K_1]:
                return 'level_1'
            elif keys[pygame.K_2]:
                return 'level_2'
            elif keys[pygame.K_3]:
                return 'level_3'
            elif keys[pygame.K_4]:
                return 'level_4'
        return '-'

    def draw_text(self, text, color, x, y):
        text_surf = self.font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))

    def run(self):
        self.draw_text("Level Select", conf.WHITE, 100, 100)
