import pygame as pg
import random
from pygame.sprite import *

class Item(Sprite):
    """A class to manage speed item droped from the alien"""
    def __init__(self, setting, screen, type, posx, posy):
        """Create a item object at the aliens current position"""
        super(Item, self).__init__()
        self.screen = screen

        #add item types if you want
        if(type==1):
            self.image = pg.image.load('gfx/item_heal.png')

        self.type = type

        self.rect = self.image.get_rect()

        #Create a collision mask
        self.mask = pg.mask.from_surface(self.image)

        #Create a items rect at (0,0)+-5
        ##self.rect = pg.Rect(0, 0, setting.bulletWidth, setting.bulletHeight)
        self.rect.x = posx
        self.rect.y = posy

        #store the item position as a decimal value
        self.y = float(self.rect.y)

        self.itemSpeed = setting.bulletSpeed * 0.3


    def update(self):
        """Move the item -y up the screen"""
        #update the decimal position of the item
        self.y += self.itemSpeed
        #Update the rect position
        self.rect.y = self.y


    def drawitem(self):
        """Draw the item to the screen"""
        #pg.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)
