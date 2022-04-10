import sys
import pygame as pg


class Stats():
    def __init__(self):
        self.frames_exit = 0
        self.frames_exit1 = 0
        self.first_iteration = True
        self.not_first_iteration = False

    def lose_round(self, screen):
        '''Завершение игры, окно поражения'''
        screen.blit(pg.image.load('img/game_over.png'), (0, 0))
        pg.display.flip()
        pg.time.delay(4000)
        sys.exit()

    def win_round(self, screen):
        '''Завершение игры, окно выигрыша'''
        screen.blit(pg.image.load('img/win.png'), (0, 0))
        pg.display.flip()
        pg.time.delay(4000)
        sys.exit()
