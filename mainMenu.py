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
                    buttonAction(stats, selectedName)
            elif event.key == 46:
                setting.shipLimit += 1
            elif event.key == 44 and setting.shipLimit > 1:
                setting.shipLimit -= 1
            elif event.key == pg.K_ESCAPE:
                sounds.button_click_sound.play()
                pg.time.delay(300)
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
                    buttonAction(stats, mouseBtnName)


def buttonAction(stats, selectedName):
    if selectedName == 'play':
        stats.setGameLoop('playMenu')
    elif selectedName == 'twoPlay':
        stats.setGameLoop('twoPlayer')
    elif selectedName == 'about':
        stats.setGameLoop('mainAbout')
    elif selectedName == 'settings':
        stats.setGameLoop('settingsMenu')
    elif selectedName == 'quit':
        pg.time.delay(300)
        sys.exit()


def drawMenu(setting, screen, sb, bMenu, bgImage, bgImageRect):
    """Draw the menu and all of its elements"""
    screen.fill(setting.bgColor)
    screen.blit(bgImage, bgImageRect)
    bMenu.drawMenu()
    pg.display.flip()