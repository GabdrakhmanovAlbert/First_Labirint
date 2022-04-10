import heroes
import pygame as pg
import random


class Wall(pg.sprite.Sprite):
    '''Видимая стена, барьер для врагов и игрока'''

    def __init__(self, screen, color, width, height, x, y):
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)
        self.screen = screen
        self.color = color
        # границы стены
        # по x
        self.left_border = x
        self.right_border = x + width
        # по y
        self.top_border = y
        self.down_border = y + height

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class InvisibleWall(pg.sprite.Sprite):
    '''Невидимые спрайты (100 на 1 px) для осуществления поворотов пришельцев в сложных местах'''

    def __init__(self, screen, x, y, angle):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.img = pg.transform.rotate(pg.image.load('img/empty.png'), angle)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        '''Отрисовка невидимого спрайта'''
        self.screen.blit(self.img, self.rect)


def create_labirint(screen, color):
    '''Первый вариант лабиринта'''
    walls = pg.sprite.Group()
    invis_walls = pg.sprite.Group()
    # здесь хранятся для каждой стены - [ширина, высота, х, y]
    stats_walls = [
        [25, 225, 100, 0],
        [25, 175, 100, 325],
        [125, 25, 0, 500],
        [25, 175, 100, 525],
        [100, 25, 125, 675],
        [25, 75, 250, 0],
        [25, 175, 400, 0],
        [200, 25, 225, 175],
        [25, 150, 275, 325],
        [375, 25, 225, 475],
        [25, 75, 225, 500],
        [25, 50, 400, 300],
        [200, 25, 400, 350],
        [25, 75, 425, 600],
        [125, 25, 325, 675],
        [150, 25, 550, 100],
        [25, 150, 525, 100],
        [50, 25, 550, 225],
        [25, 75, 575, 500],
        [25, 125, 575, 675]
    ]
    # здесь инфа о каждой невидимой стене [x, y, угол наклона]
    stats_invisible_walls = [
        [150, 75, 0],
        [0, 225, 0],
        [225, 225, 90],
        [0, 325, 0],
        [600, 575, 0],
        [600, 675, 0],
        [225, 700, 90],
        [325, 700, 90],
        [600, 250, 0],
        [600, 350, 0],
        [475, 575, 0],
        [475, 675, 0]
    ]

    # добавление видимых
    for arguments in stats_walls:
        wall = Wall(screen, color,
                    arguments[0], arguments[1], arguments[2], arguments[3])
        walls.add(wall)
    del arguments

    # добавление невидимых
    for arguments in stats_invisible_walls:
        invis_wall = InvisibleWall(
            screen, arguments[0], arguments[1], arguments[2])
        invis_walls.add(invis_wall)

    return (walls, invis_walls)
