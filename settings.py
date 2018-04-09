import pygame as pg

import utilityFunctions

getInvertedRGB = utilityFunctions.getInvertedRGB


class Settings():

    """A class to store all settings for game"""

    def __init__(self):
        """Initialize the class"""
        self.windowCaption = 'Galtron'
        self.screenWidth = 550
        self.screenHeight = 650
        self.bgColor = (20, 20, 20)

        self.gameOverImage = pg.image.load("gfx/gameover.png")
        self.gameOverImage = pg.transform.scale(self.gameOverImage,
                                                (self.screenWidth - 40, self.gameOverImage.get_height()))
        # Ultimate settings
        self.ultimateGaugeIncrement = 3

        # Ships speed
        self.shipLimit = 3

        # Bullet settings
        self.bulletWidth = 3
        self.bulletHeight = 15
        self.bulletColor = (60, 60, 60)

        # How quickly the game speeds up
        self.speedUp = 1.1
        self.scoreSpeedUp = 5

        # GameSpeedLimit
        self.Limit = 0
        self.globalGameSpeed = 1

        self.initDynamicSettings()
        # Interception settings
        self.checkBtnPressed = 0
        self.interception = False
        # New Level Starts at this time
        self.newStartTime = 0

        # Game Level
        self.gameLevel = 'normal'

        # Alien shoot speed
        self.shootTimer = 50

        #item probability %
        self.probabilityHeal = 10

        #invincibile time
        self.invincibileTime = 2000

        
    def invertColor(self):
        self.bgColor = getInvertedRGB(self.bgColor)
        self.bulletColor = getInvertedRGB(self.bulletColor)


    def initDynamicSettings(self):
        self.shipSpeed = 2.5
        self.bulletSpeed = 4
        self.alienSpeed = 1
        self.fleetDropSpeed = 5
        self.fleetDir = 1
        self.alienPoints = 10

    def increaseSpeed(self):
        """Increase the speed settings"""
        if self.alienSpeed <= 1.5:
            self.alienSpeed *= self.speedUp
            self.fleetDropSpeed *= self.speedUp


            # self.alienPoints = int(self.alienPoints * self.scoreSpeedUp)
            # self.alienPoints = int(self.alienPoints + self.scoreSpeedUp)

    def setIncreaseScoreSpeed(self, level):
        self.alienPoints = int(self.alienPoints + ((level - 1) * 10))

        self.alienPoints = int(self.alienPoints + self.scoreSpeedUp)


    def halfspeed(self):
        if self.Limit >= -1 and self.shipSpeed > 0 and self.bulletSpeed > 0 and self.alienSpeed > 0 and self.fleetDropSpeed > 0:
            self.shipSpeed *= 0.5
            self.bulletSpeed *= 0.5
            self.alienSpeed *= 0.5
            self.fleetDropSpeed *= 0.5
            self.alienPoints *= 0.5  # nerf earning points in lower speed
            self.globalGameSpeed *= 0.5
            self.Limit -= 1

    def doublespeed(self):
        self.shipSpeed *= 1.3
        self.bulletSpeed *= 1.3
        self.alienSpeed *= 1.3
        self.fleetDropSpeed *= 1.3
        self.alienPoints *= 1.3
        self.globalGameSpeed *= 1.3
        self.Limit += 1
