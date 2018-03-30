import pygame as pg
from pygame.sprite import *


class TimeStopItem(Sprite):
    """A class to manage timestop item"""

    def __init__(self, setting, screen):
        """Create a bullet object at the ships current position"""
        super(TimeStopItem, self).__init__()
        self.screen = screen

        # load the timestop item image and set its rect attribute
        self.image = pg.image.load('gfx/ship.bmp')
        self.rect = self.image.get_rect()

        # Create a collision mask
        self.mask = pg.mask.from_surface(self.image)

        # Create a timestop item rect at (0,800)
        ##self.rect = pg.Rect(0, 0, setting.timestopitemWidth, setting.timestopitemHeight)
        screenRect = screen.get_rect()
        self.rect.centerx = (screenRect.right - screenRect.left) / 2
        self.rect.bottom = screenRect.top

        # store the bullets position as a decimal value
        self.y = float(self.rect.y)

        self.color = setting.timestopitemColor
        self.itemSpeed = setting.itemSpeed

    def update(self):
        """Move the item +y up the screen"""
        # update the decimal position of the bullet
        self.y += self.itemSpeed
        # Update the rect position
        self.rect.y = self.y

    def drawTimeStopItem(self):
        """Draw the item to the screen"""
        # pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
