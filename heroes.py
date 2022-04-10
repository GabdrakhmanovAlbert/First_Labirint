import random
import pygame as pg
import Bullets
import controls


class AbstractSprite(pg.sprite.Sprite):
    def __init__(self, screen, picture, x_y):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.img = self.convert_img(pg.image.load(picture))
        self.rect = self.img.get_rect()
        self.rect.x = x_y[0]
        self.rect.y = x_y[1]

    def output(self):
        self.screen.blit(self.img, self.rect)

    def convert_img(self, picture):
        '''Делает картинке нормальные размеры'''
        size_picture = picture.get_rect()
        if size_picture.width / size_picture.height >= 2:
            return pg.transform.scale(picture, (75, 40))
        elif size_picture.height / size_picture.width >= 2:
            return pg.transform.scale(picture, (40, 75))
        else:
            return pg.transform.scale(picture, (75, 75))


class Enemy(AbstractSprite):
    '''Враг, который сам ходит и стреляет'''

    def __init__(self, screen, picture, x_y):
        super().__init__(screen, picture, x_y)
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)
        self.directions = ('left', 'right', 'up', 'down')
        self.direction = random.choice(self.directions)
        self.speed = 1.1
        self.frames_change_direction = random.randint(1000, 500000)
        self.counter_barrier_collisions = 0

        self.frames_shoot = 100
        self.angle_bullets = [0, -90, -180, -270]

    def position_correction(self, cur_direction):
        '''Когда враг врезается в стены, края экрана, тогда отодвигает от объекта, для нормального выбора направления'''
        if cur_direction == 'left':
            self.center_x += 2
        elif cur_direction == 'right':
            self.center_x -= 2
        elif cur_direction == 'up':
            self.center_y += 2
        elif cur_direction == 'down':
            self.center_y -= 2

        self.rect.centerx = self.center_x
        self.rect.centery = self.center_y

    def set_direction(self, cur_direction):
        '''Выбирает направление дальнейшего движения'''
        self.position_correction(cur_direction)
        self.direction = random.choice(self.directions)
        while self.direction == cur_direction:
            self.direction = random.choice(self.directions)

    def collision_with_barrier(self, barriers):
        '''С вероятностью 20% враг, столкнувшись с барьером изменит направление'''
        barrier_set_direction = random.randint(1, 5)
        if pg.sprite.spritecollideany(self, barriers):
            if (self.counter_barrier_collisions == 0) and (barrier_set_direction == 1):
                self.set_direction(self.direction)
            self.counter_barrier_collisions += 1
        else:
            self.counter_barrier_collisions = 0

    def collision_with_other_enemies(self, enemies):
        '''Меняет направление при коллизии с врагами'''
        collision = pg.sprite.spritecollide(self, enemies, False)
        if len(collision) > 1:
            self.set_direction(self.direction)

    def collision_with_walls(self, walls):
        '''Враг столкнувшись со стеной или краем экрана меняет направление'''
        if pg.sprite.spritecollideany(self, walls) or \
           self.rect.top < self.screen_rect.top or \
           self.rect.left < self.screen_rect.left or \
           self.rect.right > self.screen_rect.right or \
           self.rect.bottom > self.screen_rect.bottom:

            self.set_direction(self.direction)

    def moving(self, walls, barriers, enemies):
        '''Движение врага: (движется до препятствия или конца экрана, затем меняет направление(set_direction))'''

        self.collision_with_barrier(barriers)

        self.collision_with_walls(walls)

        self.collision_with_other_enemies(enemies)

        if self.frames_change_direction == 0:
            # случайное, но очень редкое изменение направления, добавил по фану :)
            self.frames_change_direction = random.randint(1000, 500000)
            self.set_direction(self.direction)
        else:
            # само движение
            if self.direction == 'left':
                self.center_x -= self.speed
            elif self.direction == 'right':
                self.center_x += self.speed
            elif self.direction == 'up':
                self.center_y -= self.speed
            elif self.direction == 'down':
                self.center_y += self.speed

            self.rect.centerx = self.center_x
            self.rect.centery = self.center_y
            self.frames_change_direction -= 1

    def may_shoot(self, screen, enemy, bullets):
        '''Создание пуль врага'''
        if self.frames_shoot == 0:
            self.frames_shoot = 40
            bullets.add(Bullets.EnemyBullet(
                screen, random.choice(self.angle_bullets), enemy))
        else:
            self.frames_shoot -= 1


class Player(AbstractSprite):
    '''Игрок, который умеет ходить'''

    def __init__(self, screen, picture, x_y):
        super().__init__(screen, picture, x_y)
        self.lock_events = False
        # Движение игрока
        self.is_alive = True
        self.speed = 1.2
        self.lock_moving()
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)
        self.counter_collisions = 0

    def moving(self, screen, player, walls):
        '''Движение игрока, при нажатии на клавиши'''
        if self.mUP and self.rect.top > self.screen_rect.top:
            self.center_y -= self.speed

        elif self.mDOWN and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.speed

        if self.mRIGHT and self.rect.right < self.screen_rect.right:
            self.center_x += self.speed

        elif self.mLEFT and self.rect.left > self.screen_rect.left:
            self.center_x -= self.speed

        self.rect.centery = self.center_y
        self.rect.centerx = self.center_x

    def lock_moving(self):
        '''Блокировка движения для предотвращения пересечения стен'''
        self.mUP = False
        self.mDOWN = False
        self.mRIGHT = False
        self.mLEFT = False
