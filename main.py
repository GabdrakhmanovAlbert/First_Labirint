import pygame as pg
import controls
import heroes
import random
import labirint
import Bullets
import sys
from stats import Stats


def run():
    pg.init()
    screen = pg.display.set_mode((700, 800))
    screen_rect = screen.get_rect()
    pg.display.set_caption('Лабиринт O__O')
    screen.blit(pg.image.load('img/dark_back.jpg'), (0, 0))
    stats = Stats()

    enemies_img = ['img/ghost.png', 'img/robot1.png',
                   'img/mummy.png', 'img/robot2.png', 'img/police1.png', 'img/police2.png', 'img/strange_skull.png']
    player_img = ['img/cool_human.png',
                  'img/human_angel.png', 'img/human_with_gun.png']
    exit_img = ['img/beautiful_door.png',
                'img/mysterious_door.png', 'img/opened_door.png']
    enemies_position = [[10, 10], [610, 710], [
        screen_rect.centerx - 40, screen_rect.centery - 40], [610, 10], [345, 595], [150, 10]]
    player_position = [10, 710]
    exit_position = [[0, 400], [300, 0], [435, 0], [550, 135]]

    player = heroes.Player(screen, random.choice(player_img), player_position)

    enemies = pg.sprite.Group()
    for _ in range(len(enemies_position)):
        enemy_img = random.choice(enemies_img)
        x_y = random.choice(enemies_position)
        enemies_position.remove(x_y)
        enemies.add(heroes.Enemy(screen, enemy_img, x_y))

    bullets = pg.sprite.Group()

    # возможные цвета стен
    colors = [(116, 255, 3), (160, 54, 35), (255, 255, 255)]
    # объект класса Group - содержащий стены
    walls, barriers = labirint.create_labirint(screen, random.choice(colors))

    door = heroes.AbstractSprite(screen, random.choice(
        exit_img), random.choice(exit_position))

    while True:
        controls.events(screen, player, bullets)
        controls.update_bullets(screen, bullets, enemies, player, stats)
        controls.remove_missed_bullets(screen_rect, bullets, walls)
        bullets.update()
        player.moving(screen, player, walls)
        controls.check_player_exit(player, door, screen, stats)
        controls.check_collision(screen, player, walls)
        controls.check_bugs(player)
        controls.update_enemies(screen, enemies, bullets, walls, barriers)
        controls.update_screen(screen, player, enemies,
                               walls, barriers, bullets, door)
        pg.display.update()


run()
