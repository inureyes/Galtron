import json
import os

class GameStats():
	"""Track stats for alien shooter"""
	def __init__(self, setting):
		"""initialize statistics"""
		self.setting = setting
		#Start alien invasion in an active state.
		self.gameActive = False
		self.mainMenu = True
		self.mainGame = False
		self.mainAbout = False
		self.playMenu = False
		self.twoPlayer = False
		self.paused = False
		self.score = 0
		self.level = 1
		self.highScore = 0
		#self.counter = 3
		self.resetStats()


	def resetStats(self):
		"""initialize statistics that can change during the game"""
		self.shipsLeft = self.setting.shipLimit
		self.level = 1
		self.score = 0
		self.counter = 3
		self.ultimateGauge = 0
		self.ultimatePattern = 1
		filename = 'data-files/highscore.json'
		if not os.path.isfile(filename):
			with open(filename, 'w') as f_obj:
				f_obj.write('0')

		with open(filename, 'r') as f_obj:
			self.tempScore = json.load(f_obj)
		if self.highScore >= self.tempScore:
			with open(filename, 'w') as f_obj:
				json.dump(self.highScore, f_obj)
		else:
			self.highScore = self.tempScore
