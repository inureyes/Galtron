import sys

import pygame as pg

import sounds


def checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets):
    """Respond to keypresses and mouse events."""
    for event in pg.event.get():
        # Check for quit event
        if event.type == pg.QUIT:
            sys.exit()
            # Check for key down has been pressed
        elif event.type == pg.KEYDOWN:
            # Check if down, up, enter, esc is pressed
            if event.key == pg.K_DOWN:
                sounds.control_menu.play()
                bMenu.down()
            if event.key == pg.K_UP:
                sounds.control_menu.play()
                bMenu.up()
            if event.key == pg.K_RETURN:
                sounds.select_menu.play()
                selectedName, selectedBtn = bMenu.getSelectedButton()
                if selectedBtn:
                    buttonAction(stats, selectedName, ship)
            if event.key == pg.K_ESCAPE:
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
                    buttonAction(stats, mouseBtnName, ship)


def buttonAction(stats, selectedName, ship):
    if selectedName in ('grey', 'red', 'blue'):
        color = selectedName
        shipImageFile = 'gfx/player_' + color + '.bmp'
        ship.image = pg.image.load(shipImageFile)
        stats.setGameLoop('mainGame')
    elif selectedName == 'menu':
        stats.setGameLoop('mainMenu')
    elif selectedName == 'quit':
        pg.time.delay(300)
        sys.exit()


def drawMenu(setting, screen, sb, bMenu):
    """Draw the menu and all of its elements"""
    screen.fill(setting.bgColor)
    bMenu.drawMenu()
    pg.display.flip()


def checkColor():
    return 'gfx/player_' + color + '.bmp'


def drawimg():
    img = pg.image.load('gfx/player_blue.bmp')
    return 0
