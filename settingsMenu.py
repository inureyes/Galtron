import sys

import pygame as pg

import sounds
from button import Button  # A button class that can be called for every new button
from scoreboard import Scoreboard  # Score board for points, high score, lives, level ect.
from settings import Settings

# Create a variable to change current button being selected
SmBtn = 1


def checkEvents1(setting, screen, stats, sb, playBtn, quitBtn, menuBtn, sel, ship, aliens, bullets, eBullets):
    """Respond to keypresses and mouse events."""
    global SmBtn
    for event in pg.event.get():
        # Check for quit event
        if event.type == pg.QUIT:
            sys.exit()
            # Check for key down has been pressed
        elif event.type == pg.KEYDOWN:
            # Check if down, up, enter, esc is pressed
            if event.key == pg.K_DOWN:
                if SmBtn < 3:
                    sounds.control_menu.play()
                    SmBtn += 1
                    sel.rect.y += 50
            if event.key == pg.K_UP:
                if SmBtn > 1:
                    sounds.control_menu.play()
                    SmBtn -= 1
                    sel.rect.y -= 50
            if event.key == pg.K_RETURN:
                stats.mainMenu = False
                stats.mainGame = False
                stats.twoPlayer = False
                stats.mainAbout = False
                stats.settingsMenu = False
                sounds.select_menu.play()
                if SmBtn == 1:
                    stats.mainMenu = True
                    sel.rect.centery = playBtn.rect.centery
                elif SmBtn == 2:
                    sys.exit()
                elif SmBtn == 3:
                    Button.reverseColAll()
                    setting.reverseCol()
                    sb.reverseCol()
                    stats.mainMenu = True
                    sel.rect.centery = playBtn.rect.centery
                SmBtn = 1
            if event.key == pg.K_ESCAPE:
                sys.exit()
    prepSm(setting, screen)


def prepSm(setting, screen):
    # Font settings for scoring information
    global image, rect
    image = pg.image.load('gfx/fixsettings.png')
    rect = image.get_rect()


def drawMenu(setting, screen, sb, menuBtn, quitBtn, bgcrbtn, sel):
    """Draw the menu and all of its elements"""
    global image, rect
    quitBtn.rect.y = 450
    quitBtn.msgImageRect.y = 450
    menuBtn.rect.y = 400
    menuBtn.msgImageRect.y = 400
    bgcrbtn.rect.y = 500
    bgcrbtn.msgImageRect.y = 500
    screen.fill(setting.bgColor)
    menuBtn.drawBtn()
    quitBtn.drawBtn()
    bgcrbtn.drawBtn()
    screen.blit(image, rect)
    sel.blitme()
    pg.display.flip()
