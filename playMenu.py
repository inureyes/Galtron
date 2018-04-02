import sys
import gameFunctions as gf #Event checker and update screen
import pygame as pg

setBtn = 1
color = 'grey'

#Init and load sound effects
pg.mixer.init(44100, -16, 2, 4096)
control_menu = pg.mixer.Sound("sounds/control_menu.wav")
control_menu.set_volume(0.22)
select_menu = pg.mixer.Sound("sounds/select_menu.wav")
select_menu.set_volume(0.18)
start_game = pg.mixer.Sound("sounds/start_game.wav")
start_game.set_volume(0.3)

def checkEvents(setting, screen, stats, sb, playBtn, greyBtn, redBtn, blueBtn, quitBtn, menuBtn, sel, ship, aliens, bullets, eBullets):
	"""Respond to keypresses and mouse events."""
	global setBtn , color
	for event in pg.event.get():
		#Check for quit event
		if event.type == pg.QUIT:
			sys.exit()
		#Check for key down has been pressed
		elif event.type == pg.KEYDOWN:
			#Check if down, up, enter, esc is pressed
			if event.key == pg.K_DOWN:
				if setBtn < 5:
					control_menu.play()
					setBtn += 1
					sel.rect.y += 50
			if event.key == pg.K_UP:
				if setBtn > 1:
					control_menu.play()
					setBtn -= 1
					sel.rect.y -= 50
			if event.key == pg.K_RETURN:
				if setBtn == 1:
					#default mode
					start_game.play()
					color = 'grey'
					stats.mainMenu = False
					stats.mainGame = True
					stats.playMenu = False
					stats.twoPlayer = False
					stats.mainAbout = False
					setBtn = 1
					sel.rect.centery = playBtn.rect.centery
				elif setBtn == 2:
					start_game.play()
					color = 'red'
					stats.mainMenu = False
					stats.mainGame = True
					stats.playMenu = False
					stats.twoPlayer = False
					stats.mainAbout = False
					setBtn = 1
					sel.rect.centery = playBtn.rect.centery
				elif setBtn == 3:
					start_game.play()
					color = 'blue'
					stats.mainMenu = False
					stats.mainGame = True
					stats.playMenu = False
					stats.twoPlayer = False
					stats.mainAbout = False
					setBtn = 1
					sel.rect.centery = playBtn.rect.centery
				elif setBtn == 4:
					#menu btn
					select_menu.play()
					stats.mainMenu = True
					stats.mainGame = False
					stats.playMenu = False
					stats.twoPlayer = False
					stats.mainAbout = False
					setBtn = 1
					sel.rect.centery = playBtn.rect.centery
				elif setBtn == 5:
					sys.exit()
			if event.key == pg.K_ESCAPE:
				sys.exit()

def drawMenu(setting, screen, sb, greyBtn, redBtn, blueBtn, menuBtn, quitBtn, sel):
    """Draw the menu and all of its elements"""
    global image, rect
    screen.fill(setting.bgColor)
    menuBtn.rect.y = 350
    menuBtn.msgImageRect.y = 350
    quitBtn.rect.y = 400
    quitBtn.msgImageRect.y = 400
    menuBtn.drawBtn()
    quitBtn.drawBtn()
    greyBtn.drawBtn()
    redBtn.drawBtn()
    blueBtn.drawBtn()
    sel.blitme()
    pg.display.flip()

def checkColor():
	return 'gfx/player_'+color+'.bmp'
