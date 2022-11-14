import pygame, sys
import src.codes.config as conf


class MainMenu:
    def __init__(self, screen):
        self.display_screen = screen

        self.font = pygame.font.Font(conf.chary_font, 80)
        self.index = 0  # 0: start, 1: level_select 2: exit
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
                    return 'level'
                elif self.index == 1:
                    return 'level_select'
                elif self.index == 2:
                    pygame.quit()
                    sys.exit()
            elif keys[pygame.K_UP]:
                self.index -= 1
            elif keys[pygame.K_DOWN]:
                self.index += 1
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        self.index %= 3  # restricts index to 0-2
        return ''

    def run(self):
        self.draw_text_box("START", 100, 600, 100, 0)
        self.draw_text_box("SELECT LEVELS", 300, 600, 100, 1)
        self.draw_text_box("EXIT", 500, 600, 100, 2)
