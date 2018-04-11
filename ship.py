import pygame as pg
from pygame.sprite import *

import math
from bullet import Bullet
from playMenu import *



class Ship(Sprite):
    """Class of a player ship"""

    def __init__(self, setting, screen):
        """Initialize the ship and set its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.setting = setting

        # Load the ship image and its rect.
        self.imagesPath = (
            'gfx/player_ship/player_ship_left4.png',
            'gfx/player_ship/player_ship_left3.png',
            'gfx/player_ship/player_ship_left2.png',
            'gfx/player_ship/player_ship_left1.png',
            'gfx/player_ship/player_ship.png',
            'gfx/player_ship/player_ship_right1.png',
            'gfx/player_ship/player_ship_right2.png',
            'gfx/player_ship/player_ship_right3.png',
            'gfx/player_ship/player_ship_right4.png')
        self.images = []
        for path in self.imagesPath:
            img = pg.image.load(path)
            self.images.append(img)
        self.imgCenter = 4
        self.imgMaxLR = 4
        self.inclination = 0
        self.maxInclination = 8

        self.image = self.images[self.imgCenter]
        self.rect = self.image.get_rect()
        self.screenRect = screen.get_rect()

        # Create a collision mask
        self.mask = pg.mask.from_surface(self.image)

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screenRect.centerx
        self.rect.centery = self.screenRect.centery + self.screenRect.bottom / 2 - self.rect.height
        self.rect.bottom = self.screenRect.bottom - 10

        self.center = float(self.rect.centerx)
        self.right = self.screenRect.right
        self.left = self.screenRect.left
        self.centery = float(self.rect.centery)

        # Movement flag
        self.movingRight = False
        self.movingLeft = False
        self.movingUp = False
        self.movingDown = False

        # about shoot
        self.shoot = False
        self.nextShootTime = 0
        self.fireRate = 1000 / 5  # 5shoots per sec
        self.trajectory = 0

        self.chargeGaugeStartTime = 0
        self.fullChargeTime = 2500
        self.chargeGauge = 0

    def update(self, bullets, aliens, ):
        """Update the ships position"""
        if self.movingRight and self.rect.right < self.screenRect.right:
            self.center += self.setting.shipSpeed
            if self.inclination < self.maxInclination:
                self.inclination += 1
        if self.movingLeft and self.rect.left > 1:
            self.center -= self.setting.shipSpeed
            if -self.maxInclination < self.inclination:
                self.inclination -= 1
        if (not self.movingLeft) and (not self.movingRight):
            if 0 < self.inclination:
                self.inclination -= 1
            elif self.inclination < 0:
                self.inclination += 1
        if self.movingRight and self.rect.right >= self.screenRect.right:
            self.center = 1.0
        if self.movingLeft and self.rect.left <= 1:
            self.center = self.screenRect.right
        if self.movingUp and self.rect.top > self.screenRect.top + self.rect.height + 10:
            self.centery -= self.setting.shipSpeed
        if self.movingDown and self.rect.bottom < self.screenRect.bottom:
            self.centery += self.setting.shipSpeed
        if self.shoot == True:
            nowTime = pg.time.get_ticks()
            if self.checkReadyToShoot() and (len(bullets) < 10):
                sounds.attack.play()
                if (self.trajectory == 4):
                    newBullet0 = Bullet(self.setting, self.screen, self, 0)
                    newBullet1 = Bullet(self.setting, self.screen, self, 1)
                    newBullet2 = Bullet(self.setting, self.screen, self, 2)
                    bullets.add(newBullet0)
                    bullets.add(newBullet1)
                    bullets.add(newBullet2)
                else:
                    newBullet = Bullet(self.setting, self.screen, self, self.trajectory)
                    bullets.add(newBullet)
                self.setNextShootTime()
        else:
            if (self.chargeGauge == 100):
                newBullet = Bullet(self.setting, self.screen, self, self.trajectory, 2)
                bullets.add(newBullet)
                self.chargeGauge = 0

                # update rect object from self.center
        self.rect.centerx = self.center
        self.rect.centery = self.centery

        imgOffset = math.ceil(abs(self.inclination / 2))
        if 0 < self.inclination:
            self.image = self.images[self.imgCenter + imgOffset]
        elif self.inclination < 0:
            self.image = self.images[self.imgCenter - imgOffset]
        else:
            self.image = self.images[self.imgCenter]

    def setNextShootTime(self):
        nowTime = pg.time.get_ticks()
        self.nextShootTime = nowTime + (self.fireRate / self.setting.globalGameSpeed)

    def checkReadyToShoot(self):
        nowTime = pg.time.get_ticks()
        return self.nextShootTime <= nowTime

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def centerShip(self):
        """Centers the ship"""
        self.center = self.screenRect.centerx
        self.centery = self.screenRect.centery + self.screenRect.bottom / 2 - self.rect.height
