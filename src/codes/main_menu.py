import pygame, sys
import src.codes.config as conf


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.font = pygame.font.Font(conf.chary_font, 80)
        self.index = 0  # 0: start, 1: level_select 2: exit
        self.up_pressed = False
        self.down_pressed = False

    def draw_text_box(self, text, color, x, y, width, height, index):
        # center buttons
        center_x = conf.screen_width / 2 - width / 2

        pad = 10
        inner_rect = pygame.Rect((center_x, y), (width, height))
        outer_rect = pygame.Rect((center_x - pad, y - pad), (width + pad * 2, height + pad * 2))
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=inner_rect.center)
        if index == self.index:
            pygame.draw.rect(self.screen, conf.GREEN, outer_rect)
        pygame.draw.rect(self.screen, conf.WHITE, inner_rect)
        self.screen.blit(text_surf, text_rect)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.up_pressed = True
        elif keys[pygame.K_DOWN]:
            self.down_pressed = True
        else:
            if self.up_pressed:
                self.index -= 1
                self.up_pressed = False
            elif self.down_pressed:
                self.index += 1
                self.down_pressed = False

        if keys[pygame.K_SPACE]:
            if self.index == 0:
                self.create_level(self.current_level)
            # elif self.state == 'level_select':

        # restrict index to 0-2
        self.index %= 3

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.index == 0:
                    return 'level'  # This should output most recent level ("level{num}")
                elif self.index == 1:
                    return 'level_select'
                elif self.index == 2:
                    pygame.quit()
                    sys.exit()
            elif keys[pygame.K_UP]:
                self.index -= 1
            elif keys[pygame.K_DOWN]:
                self.index += 1
        self.index %= 3
        return ''

    def run(self):
        # TODO: clean up draw_text_box method
        self.draw_text_box("START", conf.GREEN, 100, 100, 600, 100, 0)
        self.draw_text_box("SELECT LEVELS", conf.GREEN, 100, 300, 600, 100, 1)
        self.draw_text_box("EXIT", conf.GREEN, 100, 500, 600, 100, 2)
