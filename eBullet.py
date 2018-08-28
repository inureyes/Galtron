import pygame as pg
from pygame.sprite import *


class EBullet(Sprite):
    """A class to manage bullets fired from the alien"""

    def __init__(self, setting, screen, alien, boss_bullet=0):
        """Create a bullet object at the ships current position"""
        super(EBullet, self).__init__()
        self.screen = screen

        # load the bullet image and set its rect attribute
        self.image = pg.image.load('gfx/eBullet.png')
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
            self.rect.centerx = alien.rect.centerx - setting.screenWidth // 16
        elif self.boss_bullet == 2:
            self.rect.centerx = alien.rect.centerx + setting.screenWidth // 16
        elif self.boss_bullet == 3:
            self.rect.centerx = alien.rect.centerx - setting.screenWidth // 32
        elif self.boss_bullet == 4:
            self.rect.centerx = alien.rect.centerx + setting.screenWidth // 32
        elif self.boss_bullet == 5:
            self.rect.centerx = alien.rect.centerx - setting.screenWidth // 16 - setting.screenWidth // 32
        elif self.boss_bullet == 6:
            self.rect.centerx = alien.rect.centerx + setting.screenWidth // 16 + setting.screenWidth // 32
        # store the bullets position as a decimal value
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.setting = setting

    def update(self, alien):
        """Move the bullet -y up the screen"""
        # update the decimal position of the bullet
        ####################
        bulletSpeed = self.setting.alienbulletSpeed
        if self.boss_bullet == 0:
            if self.setting.gameLevel == 'normal':
                if alien.isboss == False:
                    bulletSpeed = self.setting.alienbulletSpeed / 2
                else:
                    bulletSpeed = self.setting.alienbulletSpeed
            elif self.setting.gameLevel == 'hard':
                bulletSpeed = self.setting.alienbulletSpeed
            self.y += bulletSpeed
        elif self.boss_bullet == 1:
            self.x -= bulletSpeed
            self.y += bulletSpeed
        elif self.boss_bullet == 2:
            self.x += bulletSpeed
            self.y += bulletSpeed
        elif self.boss_bullet == 3:
            self.x -= bulletSpeed / 2
            self.y += bulletSpeed
        elif self.boss_bullet == 4:
            self.x += bulletSpeed / 2
            self.y += bulletSpeed
        elif self.boss_bullet == 5:
            self.y += bulletSpeed
            self.x -= bulletSpeed * 1.5
        elif self.boss_bullet == 6:
            self.y += bulletSpeed
            self.x += bulletSpeed * 1.5
        # Update the rect position
        self.rect.y = self.y
        self.rect.x = self.x

    def drawBullet(self):
        # pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
