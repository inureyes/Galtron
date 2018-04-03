import pygame as pg

class Settings():
	bgColor = (20, 20, 20)
	bgColor1 = (235,235,235)
	emp1 = (0,0,0)
	bulletColor = (60, 60, 60)
	bulletColor1 = (195,195,195)
	emp2 = (0,0,0)
	"""A class to store all settings for game"""
	def __init__(self):
		"""Initialize the class"""
		self.windowCaption = 'Galtron'
		self.screenWidth = 450
		self.screenHeight = 550
		self.bgColor
		self.bg = pg.image.load("gfx/background.bmp")

		#Ships speed
		self.shipLimit = 3

		#Bullet settings
		self.bulletWidth = 3
		self.bulletHeight = 15
		self.bulletColor

		#Alien settings

		#How quickly the game speeds up
		self.speedUp = 1.1
		self.scoreSpeedUp = 1.5

		self.initDynamicSettings()

	def reverseCol():
			Settings.emp1 = Settings.bgColor
			Settings.bgColor = Settings.bgColor1
			Settings.bgColor1 = Settings.emp1
			Settings.emp2 = Settings.bulletColor
			Settings.bulletColor = Settings.bulletColor1
			Settings.bulletColor1 = Settings.emp2
	def initDynamicSettings(self):
		self.shipSpeed = 1.5
		self.bulletSpeed = 3
		self.alienSpeed = 1
		self.fleetDropSpeed = 5
		self.fleetDir = 1
		self.alienPoints = 50

	def increaseSpeed(self):
		"""Increase the speed settings"""
		#self.shipSpeed *= self.speedUp
		#self.bulletSpeed *= self.speedUp
		if self.alienSpeed <= 1.5:
			self.alienSpeed *= self.speedUp
			self.fleetDropSpeed *= self.speedUp
		self.alienPoints = int(self.alienPoints * self.scoreSpeedUp)
