import pygame as pg
from pygame.sprite import *
from timestopitem import TimeStopItem


class Ship(Sprite):
    """Class of a player ship"""

    def __init__(self, setting, screen):
        """Initialize the ship and set its starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.setting = setting

        # Load the ship image and its rect.
        self.image = pg.image.load('gfx/player.bmp')
        self.rect = self.image.get_rect()
        self.screenRect = screen.get_rect()

        # Create a collision mask
        self.mask = pg.mask.from_surface(self.image)

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screenRect.centerx
        self.rect.bottom = self.screenRect.bottom - 10

        self.center = float(self.rect.centerx)

        # Movement flag
        self.movingRight = False
        self.movingLeft = False

        self.timer = 0

    def update(self, setting, screen, timestops):
        """Update the ships position"""
        if self.movingRight and self.rect.right < self.screenRect.right:
            self.center += self.setting.shipSpeed
        if self.movingLeft and self.rect.left > 1:
            self.center -= self.setting.shipSpeed

        self.timestops = timestops
        # update rect object from self.center
        self.rect.centerx = self.center

        self.dorpTimeStopItems(setting, screen, self.timestops)

    def dorpTimeStopItems(self, setting, screen, timestops):
        if self.timer >= 5000:
            self.timer = 0
            timestopitem = TimeStopItem(setting, screen)
            timestops.add(timestopitem)

        else:
            self.timer += 1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def centerShip(self):
        """Centers the ship"""
        self.center = self.screenRect.centerx
