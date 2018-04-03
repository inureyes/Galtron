import pygame.font
from pygame.sprite import Group
from ship import Ship
from playMenu import *

class Scoreboard():

	textColor = (255, 255, 255)
	textColor1 = (0,0,0)
	emp1 = (0,0,0)
	"""A class for scorekeeping"""
	def __init__(self, setting, screen, stats):
		self.screen = screen
		self.screenRect = screen.get_rect()
		self.setting = setting
		self.stats = stats
		self.active = False

		#Font settings for scoring information
		self.textColor
		self.font = pygame.font.Font('Fonts/Square.ttf', 20)

		#Prepare the initial score image
		self.prepScore()
		self.prepHighScore()
		self.prepLevel()
		self.prepShips()

	def reverseCol():

		Scoreboard.emp1 = Scoreboard.textColor
		Scoreboard.textColor = Scoreboard.textColor1
		Scoreboard.textColor1 = Scoreboard.emp1

	def prepScore(self):
		"""Turn the score into a rendered image"""
		roundedScore = int(self.stats.score)
		scoreStr = "Score: "
		scoreStr += "{:,}".format(roundedScore)
		self.scoreImg = self.font.render(scoreStr, True, self.textColor,
			self.setting.bgColor)

		#Display the score at the top left corner
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
		#Center the highscore
		self.highScoreRect = self.highScoreImg.get_rect()
		self.highScoreRect.x = 20
		self.highScoreRect.top = self.scoreRect.top

	def prepLevel(self):
		"""Turn the level into a rendered image."""
		#self.stats.level = "LVL " + str(self.stats.level)
		self.levelImg = self.font.render("Level: " + str(self.stats.level), True,self.textColor,
			self.setting.bgColor)
		#position below the score
		self.levelRect = self.levelImg.get_rect()
		self.levelRect.right = self.scoreRect.right
		self.levelRect.top = self.scoreRect.bottom + 2

	def prepShips(self):
		"""Show how many lives are left/ships"""
		self.ships = Group()
		for shipNumber in range(self.stats.shipsLeft):
			ship = Ship(self.setting, self.screen)
			ship.image = pygame.image.load(checkColor())
			ship.rect.x = 10 + shipNumber * (ship.rect.width -10)
			ship.rect.y = self.scoreRect.bottom + 2
			self.ships.add(ship)

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
		self.ships.draw(self.screen)
