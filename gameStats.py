import json
import os

import settings


class GameStats():
    """Track stats for alien shooter"""

    def __init__(self, setting):
        """initialize statistics"""
        self.setting = setting
        # Start alien invasion in an active state.
        self.gameActive = False
        self.mainMenu = True
        self.mainGame = False
        self.mainAbout = False
        self.playMenu = False
        self.twoPlayer = False
        self.settingsMenu = False
        self.levelMenu = False
        self.speedMenu = False
        self.paused = False
        self.score = 0
        self.level = 1

        self.highScore = 0
        self.highScoreSaveFileName = 'data-files/highscore.json'
        self.resetStats()
        self.exiton = 0

        #########
        # self.gameLevel = 0

    def setGameLoop(self, loop):
        self.mainMenu = False
        self.mainGame = False
        self.mainAbout = False
        self.playMenu = False
        self.twoPlayer = False
        self.settingsMenu = False
        ###########
        self.levelMenu = False
        self.speedMenu = False

        if loop == 'mainMenu':
            self.mainMenu = True
        elif loop == 'mainGame':
            self.mainGame = True
        elif loop == 'mainAbout':
            self.mainAbout = True
        elif loop == 'playMenu':
            self.playMenu = True
        elif loop == 'twoPlayer':
            self.twoPlayer = True
        elif loop == 'settingsMenu':
            self.settingsMenu = True
        ###################
        elif loop == 'levelMenu':
            self.levelMenu = True
        elif loop == 'speedMenu':
            self.speedMenu = True

    def resetStats(self):
        settingS = settings.Settings()
        """initialize statistics that can change during the game"""
        self.shipsLeft = self.setting.shipLimit
        self.level = 1
        self.score = 0
        self.counter = 3
        self.ultimateGauge = 0
        self.ultimatePattern = 1
        settingS.initDynamicSettings()
        self.tempScore = self.loadHighScore()
        if self.highScore >= self.tempScore:
            self.saveHighScore()
        else:
            self.highScore = self.tempScore

    def loadHighScore(self):
        score = 0
        if not os.path.isfile(self.highScoreSaveFileName):
            with open(self.highScoreSaveFileName, 'w') as f_obj:
                f_obj.write('0')
        with open(self.highScoreSaveFileName, 'r') as f_obj:
            score = json.load(f_obj)
        return score

    def saveHighScore(self):
        with open(self.highScoreSaveFileName, 'w') as f_obj:
            json.dump(self.highScore, f_obj)
