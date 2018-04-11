# Created by Matt Boan
import pygame as pg
from pygame.sprite import Group

import about as About
import gameFunctions as gf  # Event checker and update screen
import intro  # intro video making
import mainMenu as mm  # Main menu
import levelMenu as lm  # select game level(hard/easy)
import playMenu as pm  # choosing ship color
import settingsMenu as sm
import twoPlayer as tp  # two player mode
from animations import Explosions
from buttonMenu import ButtonMenu
from background import BackgroundManager
from gameStats import GameStats  # Game stats that are changed during the duration of the game
from scoreboard import Scoreboard  # Score board for points, high score, lives, level ect.
# import self made classes
from settings import Settings
from ship import Ship


def runGame():
    # Initialize game and create a window
    pg.init()
    # create a new object using the settings class
    setting = Settings()
    # creaete a new object from pygame display
    screen = pg.display.set_mode((setting.screenWidth, setting.screenHeight))

    # intro
    intro.introimages()

    # set window caption using settings obj
    pg.display.set_caption(setting.windowCaption)

    bMenu = ButtonMenu(screen)
    bMenu.addButton("play", "PLAY")
    bMenu.addButton("menu", "MENU")
    bMenu.addButton("twoPlay", "2PVS")
    bMenu.addButton("settings", "SETTINGS")
    bMenu.addButton("invert", "INVERT")
    bMenu.addButton("about", "ABOUT")
    bMenu.addButton("quit", "QUIT")
    bMenu.addButton("grey", "GREY")
    bMenu.addButton("red", "RED")
    bMenu.addButton("blue", "BLUE")
    bMenu.addButton("retry", "RETRY")
    bMenu.addButton("hard", "HARD")
    bMenu.addButton("normal", "NORMAL")

    mainMenuButtons = ["play", "about", "settings", "quit"] # delete "twoPlay"
    playMenuButtons = ["grey", "red", "blue", "menu", "quit"]
    levelMenuButtons = ["hard", "normal", "quit"]
    mainGameButtons = ["play", "menu", "quit"]
    aboutButtons = ["menu", "quit"]
    settingsMenuButtons = ["menu", "invert", "quit"]

    bgManager = BackgroundManager(screen)
    bgManager.setFillColor((0, 0, 0))
    bgManager.addBackground("universe_1", "gfx/backgrounds/stars_back.png", 0, 1)
    bgManager.addBackground("universe_1", "gfx/backgrounds/stars_front.png", 0, 1.5)
    bgManager.selectBackground("universe_1")

    # Create an instance to stor game stats
    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)

    # Make a ship
    ship = Ship(setting, screen)
    # Ships for two player
    ship1 = Ship(setting, screen)
    ship2 = Ship(setting, screen)

    #make a group of items to store
    items = Group()

    # make a group of bullets to store
    bullets = Group()
    charged_bullets = Group()
    eBullets = Group()
    setting.explosions = Explosions()

    # Make an alien
    aliens = Group()
    gf.createFleet(setting, stats, screen, ship, aliens)
    pg.display.set_icon(pg.transform.scale(ship.image, (32, 32)))

    bgImage = pg.image.load('gfx/title_c.png')
    bgImage = pg.transform.scale(bgImage, (setting.screenWidth, setting.screenHeight))
    bgImageRect = bgImage.get_rect()

    aboutImage = pg.image.load('gfx/About_modify2.png')
    aboutImage = pg.transform.scale(aboutImage, (setting.screenWidth, setting.screenHeight))
    aboutImageRect = aboutImage.get_rect()

    # plays bgm
    pg.mixer.music.load("sound_bgms/galtron.mp3")
    pg.mixer.music.set_volume(0.25)
    pg.mixer.music.play(-1)

    rungame = True

    # Set the two while loops to start mainMenu first
    while rungame:
        # Set to true to run main game loop
        bMenu.setMenuButtons(mainMenuButtons)
        while stats.mainMenu:
            mm.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            mm.drawMenu(setting, screen, sb, bMenu, bgImage, bgImageRect)

        bMenu.setMenuButtons(levelMenuButtons)
        while stats.levelMenu:
            lm.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            lm.drawMenu(setting, screen, sb, bMenu, bgImage, bgImageRect)

        bMenu.setMenuButtons(playMenuButtons)
        while stats.playMenu:
            pm.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            pm.drawMenu(setting, screen, sb, bMenu)

        bMenu.setMenuButtons(mainGameButtons)

        while stats.mainGame:
            # Game functions
            gf.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets, charged_bullets)  # Check for events
            # Reset Game
            if gf.reset == 1:
                gf.reset = 0
                pg.register_quit(runGame())
            if stats.gameActive:
                gf.updateAliens(setting, stats, sb, screen, ship, aliens, bullets, eBullets)  # Update aliens
                gf.updateBullets(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, items) # Update collisions
                gf.updateItems(setting, screen, stats, sb, ship, aliens, bullets, eBullets, items)
                ship.update(bullets, aliens)  # update the ship
                # Update the screen
            gf.updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, bMenu, bgManager, items)

        bMenu.setMenuButtons(aboutButtons)
        bMenu.setPos(None, 500)

        while stats.mainAbout:
            About.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            About.drawMenu(setting, screen, sb, bMenu, aboutImage, aboutImageRect)

        while stats.twoPlayer:
            tp.checkEvents(setting, screen, stats, sb, bMenu, bullets, aliens, eBullets, ship1, ship2)
            if stats.gameActive:
                ship1.update(bullets, aliens)
                ship2.update(bullets, aliens)
                tp.updateBullets(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets, items)
            tp.updateScreen(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets, bMenu, items)

        bMenu.setMenuButtons(settingsMenuButtons)

        while stats.settingsMenu:
            sm.checkEvents1(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            sm.drawMenu(setting, screen, sb, bMenu)

        while stats.mainGame:
            if rungame == True:
                print("test")


# init bgm mixer
pg.mixer.pre_init(44100, 16, 2, 4096)
pg.mixer.init(44100, -16, 2, 4096)
# run the runGame method to run the game

runGame()
