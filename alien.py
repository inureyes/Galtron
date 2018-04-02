import pygame as pg
from pygame.sprite import Sprite
from time import sleep
from eBullet import EBullet


class Alien(Sprite):
	"""A class to represent a single alien in the fleet"""
	def __init__(self, setting, screen):
		"""Initialize the alien and set its starting point"""
		super(Alien, self).__init__()
		self.screen = screen
		self.setting = setting

		#load the alien image and set its rect attribute
		self.image = pg.image.load('gfx/alien3.png')
		self.rect = self.image.get_rect()

		#start each new alien near the top left of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the aliens exact position
		self.x = float(self.rect.x)

		#timer for shooting
		self.timer = 0

	def checkEdges(self):
		"""Returns True if alien is at the edge of screen"""
		screenRect = self.screen.get_rect()
		if self.rect.right >= screenRect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def checkBottom(self):
		"""Returns True if alien is at the bottom of screen"""
		screenRect = self.screen.get_rect()
		if self.rect.bottom >= screenRect.bottom:
			return True

	def update(self, setting, screen, ship, aliens, eBullets):
		"""Move the alien right or left"""
		self.ship = ship
		self.aliens = aliens
		self.eBullets = eBullets
		self.x += (self.setting.alienSpeed * self.setting.fleetDir)
		self.rect.x = self.x
		self.shoot(setting, screen, self.ship, self.aliens, self.eBullets)

	def shoot(self, setting, screen, ship, aliens, eBullets):
<<<<<<< HEAD
		# add enemy_shooting_sound
		enemy_shoot_sound = pg.mixer.Sound('./sound_effect/enemy_shot.wav')
		if self.rect.centerx == self.ship.rect.centerx and len(eBullets) <= 4:
=======
		if self.rect.centerx >= self.ship.rect.centerx and len(eBullets) <= 4:
>>>>>>> fa0c7bdd1b7f7f05207f4d8e836529072aaeb4a4
			if self.timer >= 50:
				pg.mixer.Sound.play(enemy_shoot_sound)
				self.timer = 0
				newBullet = EBullet(setting, screen, self)
				eBullets.add(newBullet)
			self.timer += 1


	def blitme(self):
		"""draw hte alien"""
		self.screen.blit(self.image, self.rect)
