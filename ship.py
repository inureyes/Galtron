import pygame as pg
from pygame.sprite import *

class Ship(Sprite):
	"""Class of a player ship"""
	def __init__(self, setting, screen):
		"""Initialize the ship and set its starting position"""
		super(Ship, self).__init__()
		self.screen = screen
		self.setting = setting

		#Load the ship image and its rect.
		self.image = pg.image.load('gfx/player.bmp')
		self.rect = self.image.get_rect()
		self.screenRect = screen.get_rect()

		#Create a collision mask
		self.mask = pg.mask.from_surface(self.image)

		#Start each new ship at the bottom center of the screen.
		self.rect.centerx = self.screenRect.centerx
		self.rect.centery = self.screenRect.centery + self.screenRect.bottom / 2 - self.rect.height
		self.rect.bottom = self.screenRect.bottom - 10

		self.center = float(self.rect.centerx)
		self.centery = float(self.rect.centery)

		#Movement flag
		self.movingRight = False
		self.movingLeft = False
		self.movingUp = False
		self.movingDown = False

	def update(self):
		"""Update the ships position"""
		if self.movingRight and self.rect.right < self.screenRect.right:
			self.center += self.setting.shipSpeed
		if self.movingLeft and self.rect.left > 1:
			self.center -= self.setting.shipSpeed
		if self.movingRight and self.rect.right >= self.screenRect.right:
			self.center = 1.0
		if self.movingLeft and self.rect.left <= 1:
			self.center = self.screenRect.right
		if self.movingUp and self.rect.top > self.screenRect.top + self.rect.height + 10:
			self.centery -= self.setting.shipSpeed
		if self.movingDown and self.rect.bottom < self.screenRect.bottom:
			self.centery += self.setting.shipSpeed


		#update rect object from self.center
		self.rect.centerx = self.center
		self.rect.centery = self.centery

	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)

	def centerShip(self):
		"""Centers the ship"""
		self.center = self.screenRect.centerx
		self.centery = self.screenRect.centery + self.screenRect.bottom / 2 - self.rect.height