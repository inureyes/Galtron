# Created by Matt Boan
import pygame as pg
from pygame.sprite import Group

import about as About
import gameFunctions as gf  # Event checker and update screen
<<<<<<< HEAD
import intro  # intro video making
<<<<<<< HEAD
=======
import intro #intro video making
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
import mainMenu as mm  # Main menu
=======
>>>>>>> 23d39c5cce5e8ed43c7a7b9b2607b84c39de53a7
import levelMenu as lm  # select game level(hard/easy)
import mainMenu as mm  # Main menu
import playMenu as pm  # choosing ship color
import settingsMenu as sm
import sounds
import speedMenu as spm
import twoPlayer as tp  # two player mode
from animations import Explosions
from background import BackgroundManager
from buttonMenu import ButtonMenu
from gameStats import GameStats  # Game stats that are changed during the duration of the game
from scoreboard import Scoreboard  # Score board for points, high score, lives, level ect.
<<<<<<< HEAD
=======
from selector import Selector  # Import the main menu selector
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
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

<<<<<<< HEAD
    # intro
=======
    #intro
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
    intro.introimages()

    # set window caption using settings obj
    pg.display.set_caption(setting.windowCaption)

<<<<<<< HEAD
    bMenu = ButtonMenu(screen)
    bMenu.addButton("play", "PLAY")
    bMenu.addButton("menu", "BACK")
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
    bMenu.addButton("back", "MENU")
    bMenu.addButton("speed setting", "SPEED")
    bMenu.addButton("fast", "FAST")
    bMenu.addButton("middle", "MIDDLE")
    bMenu.addButton("slow", "SLOW")
    bMenu.addButton("yes", "YES")
    bMenu.addButton("no", "NO")
    bMenu.addButton("interception", "INTERCEPT")

    bMenu.addButton("sound", "SOUND")
    bMenu.addButton("loud", "LOUD")
    bMenu.addButton("low", "LOW")

    mainMenuButtons = ["play", "about", "settings", "quit"]  # delete "twoPlay"
    playMenuButtons = ["grey", "red", "blue", "menu", "quit"]
    levelMenuButtons = ["hard", "normal", "back", "quit"]

    mainGameButtons = ["play", "menu", "quit"]
    aboutButtons = ["menu", "quit"]

    soundButtons = ["loud", "low", "menu"]

    settingsMenuButtons = ["menu", "invert", "speed setting", "interception", "quit"]
    speedButtons = ["menu", "fast", "middle", "slow"]
    settingsMenuButtons = ["menu", "invert","speed setting","sound","quit"]
    speedButtons = ["fast","middle","slow","menu"]

    soundButtons =["loud","low","menu"]
    settingsMenuButtons = ["menu", "invert","speed setting","quit"]
    speedButtons = ["fast","middle","slow"]
    settingsMenuButtons = ["menu", "invert","speed setting","quit"]
    speedButtons = ["fast","middle","slow"]
    settingsMenuButtons = ["menu", "invert","speed setting","quit"]
    speedButtons = ["fast","middle","slow"]
    settingsMenuButtons = ["menu", "invert","speed setting","quit"]
    speedButtons = ["fast","middle","slow","menu"]

    bgManager = BackgroundManager(screen)
    bgManager.setFillColor((0, 0, 0))
    bgManager.addBackground("universe_1", "gfx/backgrounds/stars_back.png", 0, 1)
    bgManager.addBackground("universe_1", "gfx/backgrounds/stars_front.png", 0, 1.5)
    bgManager.selectBackground("universe_1")
=======
    playBtn = Button(setting, screen, "PLAY", 200)
    menuBtn = Button(setting, screen, "MENU", 250)
    twoPlayBtn = Button(setting, screen, "2PVS", 250)
    setBtnbtn = Button(setting, screen, "SETTING", 400)
    bgcrbtn = Button(setting, screen, "CL REV", 500)
    aboutBtn = Button(setting, screen, "ABOUT", 300)
    quitBtn = Button(setting, screen, "QUIT", 400)
    greyBtn = Button(setting, screen, "GREY", 200)
    redBtn = Button(setting, screen, "RED", 250)
    blueBtn = Button(setting, screen, "BLUE", 300)
    # make slector for buttons
    sel = Selector(setting, screen)
    sel.rect.x = playBtn.rect.x + playBtn.width + 10
    sel.rect.centery = playBtn.rect.centery
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f

    # Create an instance to stor game stats
    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)

    # Make a ship
    ship = Ship(setting, screen)
    # Ships for two player
    ship1 = Ship(setting, screen)
    ship2 = Ship(setting, screen)

    # make a group of items to store
    items = Group()

    # make a group of bullets to store
    bullets = Group()
    charged_bullets = Group()
    eBullets = Group()
    setting.explosions = Explosions()

    # Make an alien
    aliens = Group()
<<<<<<< HEAD
    gf.createFleet(setting, stats, screen, ship, aliens)
=======
    gf.createFleet(setting, screen, ship, aliens)
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
    pg.display.set_icon(pg.transform.scale(ship.image, (32, 32)))

    bgImage = pg.image.load('gfx/title_c.png')
    bgImage = pg.transform.scale(bgImage, (setting.screenWidth, setting.screenHeight))
    bgImageRect = bgImage.get_rect()

    aboutImage = pg.image.load('gfx/About_modify2.png')
    aboutImage = pg.transform.scale(aboutImage, (setting.screenWidth, setting.screenHeight))
    aboutImageRect = aboutImage.get_rect()

    # plays bgm
    pg.mixer.music.load('sound_bgms/galtron.mp3')
    pg.mixer.music.set_volume(0.25)
    pg.mixer.music.play(-1)

    rungame = True

    sounds.stage_clear.play()
    # Set the two while loops to start mainMenu first
    while rungame:
        # Set to true to run main game loop
        bMenu.setMenuButtons(mainMenuButtons)
        while stats.mainMenu:
            if not stats.gameActive and stats.paused:
                setting.initDynamicSettings()
                stats.resetStats()
                ##stats.gameActive = True

                # Reset the alien and the bullets
                aliens.empty()
                bullets.empty()
                eBullets.empty()

                # Create a new fleet and center the ship
                gf.createFleet(setting, stats, screen, ship, aliens)
                ship.centerShip()

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

<<<<<<< HEAD
        bMenu.setMenuButtons(mainGameButtons)

=======
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
        while stats.mainGame:
            # Game functions
            gf.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets,
                           charged_bullets)  # Check for events
            # Reset Game
            if gf.reset == 1:
                gf.reset = 0
                pg.register_quit(runGame())
            if stats.gameActive:
                gf.updateAliens(setting, stats, sb, screen, ship, aliens, bullets, eBullets)  # Update aliens
                gf.updateBullets(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets,
                                 items)  # Update collisions
                gf.updateItems(setting, screen, stats, sb, ship, aliens, bullets, eBullets, items)
                ship.update(bullets, aliens)  # update the ship
                # Update the screen
<<<<<<< HEAD
<<<<<<< HEAD
            gf.updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, bMenu, bgManager, items)
=======
            gf.updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, bMenu,
                            bgManager, items)
>>>>>>> 23d39c5cce5e8ed43c7a7b9b2607b84c39de53a7

        bMenu.setMenuButtons(aboutButtons)
        bMenu.setPos(None, 500)

=======
            gf.updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, playBtn, menuBtn, quitBtn, sel)
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
        while stats.mainAbout:
            About.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            About.drawMenu(setting, screen, sb, bMenu, aboutImage, aboutImageRect)

        while stats.twoPlayer:
            tp.checkEvents(setting, screen, stats, sb, bMenu, bullets, aliens, eBullets, ship1, ship2)
            if stats.gameActive:
                ship1.update(bullets, aliens)
                ship2.update(bullets, aliens)
<<<<<<< HEAD
                tp.updateBullets(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets, items)
            tp.updateScreen(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets, bMenu, items)

        bMenu.setMenuButtons(settingsMenuButtons)

=======
                tp.updateBullets(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets)
            tp.updateScreen(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets, playBtn, menuBtn,
                            quitBtn, sel)

        #				ship1.update(bullets)
        #				ship2.update(bullets)
        #				tp.updateBullets(setting, screen, stats, ship1, ship2, bullets, eBullets)
        #			tp.updateScreen(setting, screen, stats, bullets, eBullets, playBtn, menuBtn, quitBtn, sel, ship1, ship2)
>>>>>>> 9a7759e9e5e0855c3f80663620dad6184d35898f
        while stats.settingsMenu:
            sm.checkEvents1(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            sm.drawMenu(setting, screen, sb, bMenu)

        bMenu.setMenuButtons(speedButtons)
        while stats.speedMenu:
            spm.checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets)
            spm.drawMenu(setting, screen, sb, bMenu)

        while stats.mainGame:
            if rungame == True:
                print("test")


# init bgm mixer
pg.mixer.pre_init(44100, 16, 2, 4096)
pg.mixer.init(44100, -16, 2, 4096)
# run the runGame method to run the game

runGame()
