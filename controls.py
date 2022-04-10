import pygame as pg
import sys
import Bullets
from stats import Stats


def events(screen, player, bullets):
    '''Обработка событий'''
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player.mLEFT = True
            elif event.key == pg.K_RIGHT:
                player.mRIGHT = True
            elif event.key == pg.K_UP:
                player.mUP = True
            elif event.key == pg.K_DOWN:
                player.mDOWN = True
            elif event.key == pg.K_d:
                bullets.add(Bullets.PlayerBullet(screen, 0, player))
            elif event.key == pg.K_a:
                bullets.add(Bullets.PlayerBullet(screen, -180, player))
            elif event.key == pg.K_s:
                bullets.add(Bullets.PlayerBullet(screen, -90, player))
            elif event.key == pg.K_w:
                bullets.add(Bullets.PlayerBullet(screen, -270, player))
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player.mLEFT = False
            elif event.key == pg.K_RIGHT:
                player.mRIGHT = False
            elif event.key == pg.K_UP:
                player.mUP = False
            elif event.key == pg.K_DOWN:
                player.mDOWN = False
    if player.lock_events:
        player.lock_moving()


def update_screen(screen, player, enemies, walls, barriers, bullets, door):
    '''Отрисовка объектов после каждого игрового события'''
    screen.blit(pg.image.load('img/dark_back.jpg'), (0, 0))
    for wall in walls.sprites():
        wall.draw()
    door.output()
    for invis_wall in barriers.sprites():
        invis_wall.draw()
    for bullet in bullets.sprites():
        bullet.draw()
    for enemy in enemies.sprites():
        enemy.output()
    if player.is_alive:
        player.output()
    pg.display.flip()


def update_enemies(screen, enemies, bullets, walls, barriers):
    '''Обновляет положение врагов (их передвижение, изменение направления), создаёт их пули'''
    for enemy in enemies.sprites():
        enemy.moving(walls, barriers, enemies)
        enemy.may_shoot(screen, enemy, bullets)


def check_collision(screen, player, walls):
    '''Мешает игроку проходить сквозь стены'''
    collisions = pg.sprite.spritecollide(player, walls, False, False)
    if collisions:
        player.counter_collisions += 1
        position = player.rect
        player.lock_moving()
        player.lock_events = True
        for wall in collisions:
            if wall.right_border - position.x < 10:
                player.center_x += 1
                player.rect.centerx = player.center_x
            elif wall.left_border - (position.x + position.width) < 10:
                player.center_x -= 1
                player.rect.centerx = player.center_x

            if wall.top_border - position.y < 10:
                player.center_y += 1
                player.rect.centery = player.center_y
            elif wall.down_border - (position.y + 2*position.height) < 10:
                player.center_y -= 1
                player.rect.centery = player.center_y
    else:
        player.counter_collisions = 0
        player.lock_events = False


def check_bugs(player):
    '''Исправляет баги: застревание в углах, выход за пределы игры...'''
    if player.counter_collisions > 50 or player.rect.left < player.screen_rect.left or \
            player.rect.right > player.screen_rect.right or player.rect.top < player.screen_rect.top \
            or player.rect.bottom > player.screen_rect.bottom:
        player.center_x = 47
        player.center_y = 747
        player.rect.x = player.center_x
        player.rect.y = player.center_y


def update_bullets(screen, bullets, enemies, player, stats):
    '''Движение пуль и проверка пули на коллизию'''
    for bullet in bullets:
        bullet.shoot()
        if isinstance(bullet, Bullets.EnemyBullet):
            # True - если пуля врага пересекла игрока, False - иначе
            collision = pg.sprite.collide_rect(bullet, player)
            if collision or stats.not_first_iteration:
                stats.not_first_iteration = True
                player.is_alive = False
                if stats.frames_exit1 == 0:
                    stats.frames_exit1 = 500
                    if (not stats.first_iteration):
                        stats.lose_round(screen)
                    stats.first_iteration = False
                else:
                    stats.frames_exit1 -= 1
        elif isinstance(bullet, Bullets.PlayerBullet):
            collision = pg.sprite.spritecollide(bullet, enemies, True)
            if collision:
                bullets.remove(bullet)


def remove_missed_bullets(screen_rect, bullets, walls):
    '''Удаляет пули, если коллизия со стеной или вылетели за карту'''
    # bullets == player_bullets == enemy_bullets
    for bullet in bullets.sprites():
        if bullet.rect.right < screen_rect.left or \
           bullet.rect.bottom < screen_rect.top or \
           bullet.rect.top > screen_rect.bottom or \
           bullet.rect.left > screen_rect.right:
            bullets.remove(bullet)
    collisions = pg.sprite.groupcollide(bullets, walls, True, False)


def check_player_exit(player, door, screen, stats):
    '''Проверяет, находится ли игрок на выходе в лабиринт'''
    collision = pg.sprite.collide_rect(player, door)
    if collision:
        if stats.frames_exit == 0:
            stats.frames_exit = 50
            if stats.first_iteration:
                stats.first_iteration = False
                return
            stats.win_round(screen)
        else:
            stats.frames_exit -= 1


'''
def check_collision(screen, player, walls):
    'Мешает игроку проходить сквозь стены'
    collisions = pg.sprite.spritecollide(player, walls, False, False)
    if collisions:
        position = player.rect
        for wall in collisions:
            print(position)
            print(wall.right_border)
            if wall.right_border - position.x < 10:
                player.center_x += 1
                player.rect.centerx = player.center_x
            elif wall.left_border - (position.x + position.width) < 10:
                player.center_x -= 1
                player.rect.centerx = player.center_x

            if wall.top_border - position.y < 10:
                player.center_y += 1
                player.rect.centery = player.center_y
            elif wall.down_border - (position.y + 2*position.height) < 10:
                player.center_y -= 1
                player.rect.centery = player.center_y
'''
