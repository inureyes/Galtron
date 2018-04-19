import sys

import pygame as pg

import sounds


# Create a variable to change current button being selected
def checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets):
    """Respond to keypresses and mouse events."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
            # Check for key down has been pressed
        elif event.type == pg.KEYDOWN:
            # Check if down, up, enter, esc is pressed
            if event.key == pg.K_DOWN:
                sounds.control_menu.play()
                bMenu.down()
            elif event.key == pg.K_UP:
                sounds.control_menu.play()
                bMenu.up()
            elif event.key == pg.K_RETURN:
                sounds.select_menu.play()
                selectedName, selectedBtn = bMenu.getSelectedButton()
                if selectedBtn:
                    buttonAction(stats, selectedName, setting)
            elif event.key == pg.K_ESCAPE:
                sys.exit()

        elif event.type == pg.MOUSEMOTION:
            mouseBtnName, mouseBtn = bMenu.mouseCheck(event.pos[0], event.pos[1])
            if mouseBtn is not None:
                selectedName, selectedBtn = bMenu.getSelectedButton()
                if mouseBtn is not selectedBtn:
                    sounds.control_menu.play()
                    bMenu.selectByName(mouseBtnName)

        elif event.type == pg.MOUSEBUTTONDOWN:
            pressed = pg.mouse.get_pressed()
            if (pressed[0]):
                pos = pg.mouse.get_pos()
                mouseBtnName, mouseBtn = bMenu.mouseCheck(pos[0], pos[1])
                if mouseBtn is not None:
                    sounds.select_menu.play()
                    buttonAction(stats, mouseBtnName, setting)


def buttonAction(stats, selectedName, setting):
    if selectedName == 'hard':
        setting.gameLevel = 'hard'
        stats.setGameLoop('playMenu')
    elif selectedName == 'normal':
        setting.gameLevel = 'normal'
        stats.setGameLoop('playMenu')
    elif selectedName == 'menu':
        stats.setGameLoop('mainMenu')
    elif selectedName == 'quit':
        pg.time.delay(300)
        sys.exit()
    elif selectedName == 'back':
        stats.setGameLoop('mainMenu')


def drawMenu(setting, screen, sb, bMenu, bgImage, bgImageRect):
    """Draw the menu and all of its elements"""
    screen.fill(setting.bgColor)
    screen.blit(bgImage, bgImageRect)
    bMenu.drawMenu()
    pg.display.flip()
