import pygame as pg
from animations import Explosions

class Settings():
	"""A class to store all settings for game"""
	def __init__(self):
		"""Initialize the class"""
		self.windowCaption = 'Galtron'
		self.screenWidth = 550
		self.screenHeight = 650
		self.bgColor = (20, 20, 20)
		self.image = pg.image.load("gfx/background.bmp")
		self.image = pg.transform.scale(self.image,(self.screenWidth,self.screenHeight))
		self.bg = self.image
		#Ultimate settings
		self.ultimateGaugeIncrement = 3
                		
		#Ships speed
		self.shipLimit = 5

		#Bullet settings
		self.bulletWidth = 3
		self.bulletHeight = 15
		self.bulletColor = (60, 60, 60)

		#Alien settings

		#How quickly the game speeds up
		self.speedUp = 1.1
		self.scoreSpeedUp = 5

		#GameSpeedLimit
		self.Limit = 0

		self.initDynamicSettings()

        #BackGroundChange
	def bgimg(self,number):
		number = number % 3
		if number == 0:
				self.image = pg.image.load("gfx/background2.png")
				self.bg = self.image
		elif number == 1:
				self.image = pg.image.load("gfx/background3.png")
				self.image = pg.transform.scale(self.image,(self.screenWidth,self.screenHeight))
				self.bg = self.image
		else:
				self.image = pg.image.load("gfx/background4.png")
				self.image = pg.transform.scale(self.image,(self.screenWidth,self.screenHeight))
				self.bg = self.image
        #        
	def initDynamicSettings(self):
		self.shipSpeed = 1.5
		self.bulletSpeed = 4
		self.alienSpeed = 1
		self.fleetDropSpeed = 5
		self.fleetDir = 1
		self.alienPoints = 10


	def increaseSpeed(self):
		"""Increase the speed settings"""
		#self.shipSpeed *= self.speedUp
		#self.bulletSpeed *= self.speedUp
		if self.alienSpeed <= 1.5:
			self.alienSpeed *= self.speedUp
			self.fleetDropSpeed *= self.speedUp
		self.alienPoints = int(self.alienPoints + self.scoreSpeedUp)


	def halfspeed(self):
                if self.Limit >= -1 and self.shipSpeed>0 and self.bulletSpeed>0 and self.alienSpeed>0 and self.fleetDropSpeed>0: 
                        self.shipSpeed *= 0.5
                        self.bulletSpeed *= 0.5
                        self.alienSpeed *= 0.5
                        self.fleetDropSpeed *= 0.5
                        self.fleetDir *= 0.5
                        self.alienPoints *= 0.5 # nerf earning points in lower speed
                        self.Limit -= 1

	def doublespeed(self):
                
                self.shipSpeed *= 1.3
                self.bulletSpeed *= 1.3
                self.alienSpeed *= 1.3
                self.fleetDropSpeed *= 1.3
                self.fleetDir *= 1.3
                self.alienPoints *= 1.3
                self.Limit += 1
