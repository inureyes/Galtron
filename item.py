import pygame as pg
from pygame.sprite import *


class Item(Sprite):
    """A class to manage speed item droped from the alien"""

    def __init__(self, setting, screen, stats, type, posx, posy):
        """Create a item object at the aliens current position"""
        super(Item, self).__init__()
        self.screen = screen
        self.stats = stats

        # add item types if you want
        if type == 1.1:
            self.image = pg.image.load('gfx/heal 1.png')
        elif type == 1.2:
            self.image = pg.image.load('gfx/heal 2.png')
        elif type == 1.3:
            self.image = pg.image.load('gfx/heal 3.png')
        elif type == 2.1:
            self.image = pg.image.load('gfx/time 1.png')
        elif type == 2.2:
            self.image = pg.image.load('gfx/time 2.png')
        elif type == 2.3:
            self.image = pg.image.load('gfx/time 3.png')
        elif type == 3.1:
            self.image = pg.image.load('gfx/shield 1.png')
        elif type == 3.2:
            self.image = pg.image.load('gfx/shield2.png')
        elif type == 3.3:
            self.image = pg.image.load('gfx/shield 3.png')
        elif type == 4.1:
            self.image = pg.image.load('gfx/speed 1.png')
        elif type == 4.2:
            self.image = pg.image.load('gfx/speed 2.png')
        elif type == 4.3:
            self.image = pg.image.load('gfx/speed 3.png')

        self.type = type

        self.rect = self.image.get_rect()

        # Create a collision mask
        self.mask = pg.mask.from_surface(self.image)

        # Create a items rect at (0,0)+-5
        ##self.rect = pg.Rect(0, 0, setting.bulletWidth, setting.bulletHeight)
        self.rect.x = posx
        self.rect.y = posy

        # store the item position as a decimal value
        self.y = float(self.rect.y)

        self.itemSpeed = setting.bulletSpeed * 0.3

    def update(self):
        """Move the item -y up the screen"""
        # update the decimal position of the item
        if not self.stats.paused:
            self.y += self.itemSpeed
            # Update the rect position
            self.rect.y = self.y

    def drawitem(self):
        """Draw the item to the screen"""
        # pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
