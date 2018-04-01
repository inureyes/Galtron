import pygame as pg
import math
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""
	def __init__(self, setting, screen, ship, traj):
		"""Create a bullet object at the ships current position"""
		super(Bullet, self).__init__()
		self.screen = screen

		#decide the trajectory of bullets
		self.traj = traj

		#load the bullet image and set its rect attribute
		self.image = pg.image.load('gfx/bullet.png')
		self.rect = self.image.get_rect()

		#Create a bullet rect at (0,0)
		##self.rect = pg.Rect(0, 0, setting.bulletWidth, setting.bulletHeight)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		#store the bullets position as a decimal value
		self.x = float(self.rect.centerx)
		self.y = float(self.rect.y)
		self.color = setting.bulletColor
		self.bulletSpeed = setting.bulletSpeed

	def update(self):
		"""Move the bullet -y up the screen"""
		#update the decimal position of the bullet
		if (self.traj == 0):
			self.y -= 1.5 * self.bulletSpeed
		elif (self.traj == 1):
			self.x += 0.5 * self.bulletSpeed
			self.y -= 0.5 * 2.0 * self.bulletSpeed
		elif (self.traj == 2):
			self.x -= 0.5 * self.bulletSpeed
			self.y -= 0.5 * 2.0 * self.bulletSpeed
		elif (self.traj == 3):
			self.x -= 0.8 * math.sin(0.05 * self.y)
			self.y -= 0.8 * self.bulletSpeed
		else:
			self.x += 0.8 * math.sin(0.05 * self.y)
			self.y -= 0.8 * self.bulletSpeed

		#Update the rect position899
		self.rect.centerx = self.x
		self.rect.y = self.y

	def drawBullet(self):
		"""Draw the bullet to the screen"""
		#pg.draw.rect(self.screen, self.color, self.rect)
		self.screen.blit(self.image, self.rect)
    

class SpecialBullet(Sprite):
	"""A class to manage special bullet which can be fired only by the ultimate"""
	def __init__(self, setting, screen, pos):
		"""Create the bullet object at the some position"""
		super(SpecialBullet, self).__init__()
		self.screen = screen

		#load the bullet image and set its rect attribute
		self.image = pg.image.load('gfx/bullet.png')
		self.rect = self.image.get_rect()

		#Create a bullet rect at (0,0)
		##self.rect = pg.Rect(0, 0, setting.bulletWidth, setting.bulletHeight)
		self.rect.centerx = pos[0]
		self.rect.top = pos[1]

		#store the bullets position as a decimal value
		self.y = float(self.rect.y)
		self.bulletSpeed = setting.bulletSpeed

	def update(self):
		"""Move the bullet -y up the screen"""
		#update the decimal position of the bullet
		self.y -= self.bulletSpeed
		self.rect.y = self.y


	def drawBullet(self):
		"""Draw the bullet to the screen"""
		#pg.draw.rect(self.screen, self.color, self.rect)
		self.screen.blit(self.image, self.rect)
