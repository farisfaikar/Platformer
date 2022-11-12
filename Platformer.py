import pygame, sys
import src.codes.config as conf
from src.codes.level import Level
from src.codes.level_select import LevelSelect
from src.codes.main_menu import MainMenu


# pygame setup
pygame.init()
screen = pygame.display.set_mode((conf.screen_width, conf.screen_height))
clock = pygame.time.Clock()

# Set caption, icon
pygame.display.set_caption("Platformer!")
icon = pygame.image.load('src/sprites/player/idle/1.png')
pygame.display.set_icon(icon)


class Game:
    def __init__(self):
        self.main_menu = MainMenu(screen)
        self.level_select = LevelSelect(screen)
        self.last_level = 'level_1'

    def run_main_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                state = self.main_menu.process_events(event)
                if state == 'level':
                    self.run_level(self.last_level)
                elif state == 'level_select':
                    self.run_level_select()

            self.main_menu.run()

            pygame.display.flip()
            screen.fill(conf.PURPLE)
            clock.tick(60)

    def run_level_select(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                state = self.level_select.process_events(event)
                if 'level' in state:
                    self.last_level = state
                    self.run_level(self.last_level)
                elif state == 'exit':
                    running = False

            self.level_select.run()

            pygame.display.flip()
            screen.fill(conf.BLUE)
            clock.tick(60)

    def run_level(self, state):
        self.level = Level(screen, state)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                state = self.level.process_events(event)
                if state == 'exit':
                    running = False

            self.level.run()

            pygame.display.flip()
            screen.fill(conf.RED)
            clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run_main_menu()
