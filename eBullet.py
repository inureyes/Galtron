import pygame as pg
from pygame.sprite import *


class EBullet(Sprite):
    """A class to manage bullets fired from the alien"""

    def __init__(self, setting, screen, alien, boss_bullet = 0):
        """Create a bullet object at the ships current position"""
        super(EBullet, self).__init__()
        self.screen = screen

        # load the bullet image and set its rect attribute
        self.image = pg.image.load('gfx/ebullet.bmp')
        self.rect = self.image.get_rect()
        self.boss_bullet = boss_bullet
        # Create a collision mask
        self.mask = pg.mask.from_surface(self.image)

        # Create a bullet rect at (0,0)
        ##self.rect = pg.Rect(0, 0, setting.bulletWidth, setting.bulletHeight)
        self.rect.bottom = alien.rect.bottom
        if self.boss_bullet == 0:
            self.rect.centerx = alien.rect.centerx
        elif self.boss_bullet == 1:
            self.rect.centerx = alien.rect.centerx - 10
        elif self.boss_bullet == 2:
            self.rect.centerx = alien.rect.centerx + 10
        # store the bullets position as a decimal value
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.color = setting.bulletColor
        self.setting = setting

    def update(self):
        """Move the bullet -y up the screen"""
        # update the decimal position of the bullet
        ####################
        if self.setting.gameLevel == 'normal':
            bulletSpeed = self.setting.bulletSpeed / 2
        elif self.setting.gameLevel == 'hard':
            bulletSpeed = self.setting.bulletSpeed
        self.y += bulletSpeed
        if self.boss_bullet == 1:
            self.x -= 1
        elif self.boss_bullet == 2:
            self.x += 1
        # Update the rect position
        self.rect.y = self.y
        self.rect.x = self.x

    def drawBullet(self):
        # pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
