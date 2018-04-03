import pygame as pg
from playMenu import *
from pygame.sprite import *
from bullet import Bullet
import sounds

class Ship(Sprite):
	"""Class of a player ship"""
	def __init__(self, setting, screen):
		"""Initialize the ship and set its starting position"""
		super(Ship, self).__init__()
		self.screen = screen
		self.setting = setting

		#Load the ship image and its rect.
		self.image = pg.image.load(checkColor()) #'gfx/player.bmp'
		self.rect = self.image.get_rect()
		self.screenRect = screen.get_rect()

		#Create a collision mask
		self.mask = pg.mask.from_surface(self.image)

		#Start each new ship at the bottom center of the screen.
		self.rect.centerx = self.screenRect.centerx
		self.rect.centery = self.screenRect.centery + self.screenRect.bottom / 2 - self.rect.height
		self.rect.bottom = self.screenRect.bottom - 10

		self.center = float(self.rect.centerx)
		self.right = self.screenRect.right
		self.left = self.screenRect.left
		self.centery = float(self.rect.centery)

		#Movement flag
		self.movingRight = False
		self.movingLeft = False
		self.movingUp = False
		self.movingDown = False

		#about shoot
		self.shoot = False
		self.timer = 0
		self.timer2 = 0
		self.trajectory = 0

		self.chargeGaugeStartTime = 0
		self.fullChargeTime = 2500
		self.chargeGauge = 0

	def update(self, bullets, aliens):
		self.image = pg.image.load(checkColor())
		"""Update the ships position"""
		if self.movingRight and self.rect.right < self.screenRect.right:
			self.center += self.setting.shipSpeed
			self.image = pg.transform.rotate(self.image,-45)
		if self.movingLeft and self.rect.left > 1:
			self.center -= self.setting.shipSpeed
			self.image = pg.transform.rotate(self.image,45)
		if self.movingRight and self.rect.right >= self.screenRect.right:
			self.center = 1.0
		if self.movingLeft and self.rect.left <= 1:
			self.center = self.screenRect.right
		if self.movingUp and self.rect.top > self.screenRect.top + self.rect.height + 10:
			self.centery -= self.setting.shipSpeed
		if self.movingDown and self.rect.bottom < self.screenRect.bottom:
			self.centery += self.setting.shipSpeed
		if self.shoot == True:
			if self.timer2 > 10:
				self.image = pg.transform.rotate(self.image, 0)
				if self.chargeGauge < 100:
					self.chargeGauge += 2
				else:
					self.chargeGauge = 100
				self.timer2 = 0
			else:
				self.timer2 += 1
			if self.timer > 10 and len(bullets) < 10:
				sounds.attack.play()
				if(self.trajectory == 4):
					newBullet0 = Bullet(self.setting, self.screen, self, 0)
					newBullet1 = Bullet(self.setting, self.screen, self, 1)
					newBullet2 = Bullet(self.setting, self.screen, self, 2)
					bullets.add(newBullet0)
					bullets.add(newBullet1)
					bullets.add(newBullet2)
				else:
					newBullet = Bullet(self.setting, self.screen, self, self.trajectory)
					bullets.add(newBullet)
				sounds.attack.play()
				self.timer = 0
			else:
				self.timer += 1
		else:
			if (self.chargeGauge == 100):
				newBullet = Bullet(self.setting, self.screen, self, self.trajectory, 2)
				bullets.add(newBullet)
				self.chargeGauge = 0


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
