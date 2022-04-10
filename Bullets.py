import pygame as pg


class AbstractBullet(pg.sprite.Sprite):
    '''Шаблон пули'''

    def __init__(self, screen, picture, angle, hero):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.hero = hero

        self.angle = angle
        self.speed = 5.5

        self.img = pg.transform.scale(pg.image.load(picture), (30, 15))
        self.img = pg.transform.rotate(self.img, self.angle)
        self.rect = self.img.get_rect()
        self.check_to_set_bullet()
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def draw(self):
        '''Отрисовка пуль'''
        self.screen.blit(self.img, self.rect)

    def check_to_set_bullet(self):
        '''Проверяет, куда разместить пулю по углу'''
        if self.angle == 0:
            self.rect.left = self.hero.rect.right + 5
            self.rect.centery = self.hero.rect.centery
        elif self.angle == -90:
            self.rect.centerx = self.hero.rect.centerx
            self.rect.top = self.hero.rect.bottom + 5
        elif self.angle == -180:
            self.rect.centery = self.hero.rect.centery
            self.rect.right = self.hero.rect.left - 5
        elif self.angle == -270:
            self.rect.bottom = self.hero.rect.top - 5
            self.rect.centerx = self.hero.rect.centerx

    def shoot(self):
        '''Изменение положения пули по скорости'''
        if self.angle == 0:
            self.x += self.speed
            self.rect.x = self.x
        elif self.angle == -90:
            self.y += self.speed
            self.rect.y = self.y
        elif self.angle == -180:
            self.x -= self.speed
            self.rect.x = self.x
        elif self.angle == -270:
            self.y -= self.speed
            self.rect.y = self.y


class PlayerBullet(AbstractBullet):
    '''Пуля игрока'''

    def __init__(self, screen, angle, hero):
        super().__init__(screen, 'img/player_bullet.png', angle, hero)


class EnemyBullet(AbstractBullet):
    '''Пуля врага'''

    def __init__(self, screen, angle, hero):
        super().__init__(screen, 'img/enemy_bullet.png', angle, hero)
