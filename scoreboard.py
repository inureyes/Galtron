import pygame as pg
import pygame.font
from pygame.sprite import Group

import utilityFunctions
from ship import Ship

getInvertedRGB = utilityFunctions.getInvertedRGB


class Scoreboard():
    """A class for scorekeeping"""

    def __init__(self, setting, screen, stats):
        self.screen = screen
        self.screenRect = screen.get_rect()
        self.setting = setting
        self.stats = stats
        self.active = False

        # Font settings for scoring information
        self.textColor = (255, 255, 255)
        self.font = pygame.font.Font('Fonts/Square.ttf', 20)

        self.lifeImage = pg.image.load('gfx/life.png')
        self.lifeImageRect = self.lifeImage.get_rect()

        # Prepare the initial score image
        self.prepScore()
        self.prepHighScore()
        self.prepLevel()

    def invertColor(self):
        self.textColor = getInvertedRGB(self.textColor)

    def prepScore(self):
        """Turn the score into a rendered image"""
        roundedScore = int(self.stats.score)
        scoreStr = "Score: "
        scoreStr += "{:,}".format(roundedScore)
        self.scoreImg = self.font.render(scoreStr, True, self.textColor,
                                         self.setting.bgColor)

        # Display the score at the top left corner
        self.scoreRect = self.scoreImg.get_rect()
        self.scoreRect.right = self.screenRect.right - 20
        self.scoreRect.top = 10

    def prepHighScore(self):
        """Turn the high score into a rendered image"""
        highScore = int(self.stats.highScore)
        highScoreStr = "HS: "
        highScoreStr += "{:,}".format(highScore)
        self.highScoreImg = self.font.render(highScoreStr, True, self.textColor,
                                             self.setting.bgColor)
        # Center the highscore
        self.highScoreRect = self.highScoreImg.get_rect()
        self.highScoreRect.x = 20
        self.highScoreRect.top = self.scoreRect.top

    def prepLevel(self):
        """Turn the level into a rendered image."""
        # self.stats.level = "LVL " + str(self.stats.level)
        self.levelImg = self.font.render("Level: " + str(self.stats.level), True, self.textColor,
                                         self.setting.bgColor)
        # position below the score
        self.levelRect = self.levelImg.get_rect()
        self.levelRect.right = self.scoreRect.right
        self.levelRect.top = self.scoreRect.bottom + 2

    def drawLife(self):
        """Show how many lives are left/ships"""
        self.lifeImageRect.x = 10
        self.lifeImageRect.y = self.scoreRect.bottom + 2
        for i in range(self.stats.shipsLeft):
            self.screen.blit(self.lifeImage, self.lifeImageRect)
            self.lifeImageRect.x += self.lifeImageRect.width + 10

    def prepCounter(self, active):
        self.counterImg = self.font.render(str(self.stats.counter), True, self.textColor,
                                           self.setting.bgColor)
        self.counterRect = self.counterImg.get_rect()
        self.counterRect.center = self.screenRect.center
        self.active = active

    def showScore(self):
        """Draw the score to screen"""
        self.screen.blit(self.scoreImg, self.scoreRect)
        self.screen.blit(self.highScoreImg, self.highScoreRect)
        self.screen.blit(self.levelImg, self.levelRect)
        self.drawLife()
