import pygame as pg
from pygame.sprite import *


class Selector(Sprite):
    """Class of a player ship"""

    def __init__(self, setting, screen):
        """Initialize the ship and set its starting position"""
        super(Selector, self).__init__()
        self.screen = screen
        self.setting = setting

        # Load the ship image and its rect.
        self.image = pg.image.load('gfx/sel.png')
        self.image = pg.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.screenRect = screen.get_rect()

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
