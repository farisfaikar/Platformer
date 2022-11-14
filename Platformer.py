import pygame, sys, os
import src.codes.config as conf
from src.codes.level import Level
from src.codes.level_select import LevelSelect
from src.codes.main_menu import MainMenu
from src.codes.crt import CRT


# pygame setup
pygame.init()
screen = pygame.display.set_mode((conf.screen_width, conf.screen_height))
clock = pygame.time.Clock()

# Set caption, icon
pygame.display.set_caption("PLATFORMER!")
icon = pygame.image.load('src/sprites/player/idle/1.png')
pygame.display.set_icon(icon)


class Game:
    def __init__(self):
        self.main_menu = MainMenu(screen)
        self.level_select = LevelSelect(screen)
        self.last_level_num = 1
        _, _, files = next(os.walk("src/levels"))
        self.total_levels = len(files)
        self.crt = CRT(conf.screen_width, conf.screen_height, screen)

    def run_main_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                state = self.main_menu.process_events(event)
                if state == 'level':
                    self.run_level(self.last_level_num)
                elif state == 'level_select':
                    self.run_level_select()

            self.main_menu.run()
            self.crt.draw()

            pygame.display.flip()
            screen.fill(conf.LAVANDER)
            clock.tick(60)

    def run_level_select(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                level_num = self.level_select.process_events(event)
                if level_num == -1:
                    running = False
                elif level_num == 0:
                    break
                else:
                    self.last_level_num = level_num
                    self.run_level(self.last_level_num)

            self.level_select.run()
            self.crt.draw()

            pygame.display.flip()
            screen.fill(conf.LAVANDER)
            clock.tick(60)

    def run_level(self, level_num):
        def run(level_num_):
            self.level = Level(screen, level_num_)
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    state_ = self.level.process_events(event)
                    if state_ == 'exit':
                        running = False

                status_ = self.level.run()
                self.crt.draw()

                if status_ == 'restart' or status_ == 'finished':
                    return status_

                pygame.display.flip()
                screen.fill(conf.LAVANDER)
                clock.tick(60)

        # restart level logic
        status = 'restart'
        while status == 'restart' or status == 'finished':
            status = run(level_num)
            if level_num == self.total_levels and not status == 'restart':
                status = 'exit'
            elif status == 'finished':
                level_num += 1


if __name__ == '__main__':
    game = Game()
    game.run_main_menu()
