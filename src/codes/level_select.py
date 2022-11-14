import pygame
import src.codes.config as conf


class LevelSelect:
    def __init__(self, screen):
        self.display_screen = screen
        self.font = pygame.font.Font(conf.chary_font, 80)
        self.index = 0  # 0: back, 1: level_1, 2: level_2, etc
        self.up_pressed = False
        self.down_pressed = False

    def draw_text_box(self, text, y, width, height, index, color=conf.PURPLE):
        # center buttons
        center_x = conf.screen_width / 2 - width / 2
        pad = 10
        inner_rect = pygame.Rect((center_x, y), (width, height))
        outer_rect = pygame.Rect((center_x - pad, y - pad), (width + pad * 2, height + pad * 2))

        # change color when highlighted
        if index == self.index:
            color = conf.PINK
            pygame.draw.rect(self.display_screen, conf.PINK, outer_rect)

        # draw elements
        pygame.draw.rect(self.display_screen, conf.LAVANDER, inner_rect)
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=inner_rect.center)
        self.display_screen.blit(text_surf, text_rect)

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.index == 0:
                    return -1  # goes back to main_menu
                elif self.index == 1:
                    return 1
                elif self.index == 2:
                    return 2
                elif self.index == 3:
                    return 3
                elif self.index == 4:
                    return 4
                elif self.index == 5:
                    return 5
            elif keys[pygame.K_UP]:
                self.index -= 1
            elif keys[pygame.K_DOWN]:
                self.index += 1
            elif keys[pygame.K_ESCAPE]:
                return -1
        self.index %= 6  # restricts index to 0-5
        return 0

    def run(self):
        self.draw_text_box("BACK", 50, 600, 75, 0)
        self.draw_text_box("LEVEL 1", 150, 600, 75, 1)
        self.draw_text_box("LEVEL 2", 250, 600, 75, 2)
        self.draw_text_box("LEVEL 3", 350, 600, 75, 3)
        self.draw_text_box("LEVEL 4", 450, 600, 75, 4)
        self.draw_text_box("LEVEL 5", 550, 600, 75, 5)
