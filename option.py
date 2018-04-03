import sys
import pygame as pg

#Create a variable to change current button being selected
optBtn = 1
back = False

def checkEvents(setting, screen, stats, sb, playBtn, quitBtn, menuBtn, changeCBtn, sel, ship, aliens, bullets, eBullets):
    """Respond to keypresses and mouse events."""
    global optBtn
    for event in pg.event.get():
        #Check for quit event
        if event.type == pg.QUIT:
            sys.exit()
        #Check for key down has been pressed
        elif event.type == pg.KEYDOWN:
            #Check if down, up, enter, esc is pressed
            if event.key == pg.K_DOWN:
                if optBtn < 3:
                    optBtn += 1
                    sel.rect.y += 50
            if event.key == pg.K_UP:
                if optBtn > 1:
                    optBtn -= 1
                    sel.rect.y -= 50
            if event.key == pg.K_RETURN:
                if optBtn == 1:
                    sys.exit()
                elif optBtn == 2:
                    stats.mainMenu = True
                    stats.mainGame = False
                    stats.twoPlayer = False
                    stats.mainAbout = False
                    stats.mainOption = False
                    optBtn = 1
                    sel.rect.centery = playBtn.rect.centery
                elif optBtn == 3:
                    sys.exit()
            if event.key == pg.K_ESCAPE:
                sys.exit()
    prepOption(setting, screen)

def prepOption(setting, screen):
	#Font settings for scoring information
	global image, rect
	image = pg.image.load('gfx/title.png')
	rect = image.get_rect()

# def checkChangeCBtn(setting, screen, )

def drawMenu(setting, screen, sb, changeCBtn, menuBtn, quitBtn, sel):
    """Draw the menu and all of its elements"""
    global image, rect
    quitBtn.rect.y = 500
    quitBtn.msgImageRect.y = 500
    menuBtn.rect.y = 450
    menuBtn.msgImageRect.y = 450
    chagneCBtn.rect.y = 400
    changeCBtn.msgImageRect.y = 400
    screen.fill(setting.bgColor)
    menuBtn.drawBtn()
    quitBtn.drawBtn()
    changeCBtn.drawBtn()
    screen.blit(image, rect)
    sel.blitme()
    pg.display.flip()
