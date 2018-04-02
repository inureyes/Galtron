import sys
import pygame as pg
from time import sleep
from bullet import Bullet

pauseBtnState2 = 1

#Init and load sound effects
pg.mixer.init(44100, -16, 2, 4096)
control_menu = pg.mixer.Sound("sounds/control_menu.wav")
control_menu.set_volume(0.22)
select_menu = pg.mixer.Sound("sounds/select_menu.wav")
select_menu.set_volume(0.18)
attack = pg.mixer.Sound("sounds/attack.wav")
attack.set_volume(0.08)
paused = pg.mixer.Sound("sounds/paused.wav")
paused.set_volume(0.1)

def checkEvents(setting, screen, stats, playBtn, quitBtn, sel, bullets, eBullets, ship1, ship2):
	"""Respond to keypresses and mouse events."""
	global pauseBtnState2
	for event in pg.event.get():
		#Check for quit event
		if event.type == pg.QUIT:
			sys.exit()
		#Check for key down has been pressed
		elif event.type == pg.KEYDOWN:
			checkKeydownEvents(event, setting, screen, stats, playBtn, quitBtn, sel, bullets, eBullets, pauseBtnState2, ship1, ship2)
			#Pause menu controls
			if event.key == pg.K_UP:
				if pauseBtnState2 > 1:
					control_menu.play()
					pauseBtnState2 -= 1
					sel.rect.y -= 50
			elif event.key == pg.K_DOWN:
				if pauseBtnState2 < 3:
					control_menu.play()
					pauseBtnState2 += 1
					sel.rect.y += 50	
			elif event.key == pg.K_RETURN:
				if pauseBtnState2 == 1:
					checkPlayBtn(setting, screen, stats, playBtn, sel, bullets, eBullets, ship1, ship2)
				elif pauseBtnState2 == 2:
					sel.rect.centery = playBtn.rect.centery
					pauseBtnState2 = 1
					stats.twoPlay = False
					stats.mainMenu = True
					stats.mainGame = False
					stats.mainAbout = False
				elif pauseBtnState2 == 3:
					sys.exit()	
		#Check if the key has been released
		elif event.type == pg.KEYUP:
			checkKeyupEvents(event, ship1, ship2)


def checkKeydownEvents(event, setting, screen, stats, playBtn, quitBtn, sel, bullets, eBullets, pauseBtnState2, ship1, ship2):
	"""Response to kepresses"""
	global back
	if event.key == pg.K_RIGHT:
		ship1.movingRight = True
	elif event.key == pg.K_LEFT:
		ship1.movingLeft = True
	elif event.key == pg.K_UP:
		ship1.movingUp = True
	elif event.key == pg.K_DOWN:
		ship1.movingDown = True
	elif event.key == pg.K_d:
		ship2.movingRight = True
	elif event.key == pg.K_a:
		ship2.movingLeft = True
	elif event.key == pg.K_s:
		ship2.movingDown = True
	elif event.key == pg.K_w:
		ship2.movingUp = True
	elif event.key == pg.K_RALT:
		attack.play()
		ship1.shoot = True
	elif event.key == pg.K_LALT:
		attack.play()
		ship2.shoot = True
	#Check for pause key
	elif event.key == pg.K_p:
		pause(stats)
	elif event.key == pg.K_ESCAPE:
		#Quit game
		sys.exit()

def checkKeyupEvents(event, ship1,ship2):
	"""Response to keyrealeses"""
	if event.key == pg.K_RIGHT:
		ship1.movingRight = False
	elif event.key == pg.K_LEFT:
		ship1.movingLeft = False
	elif event.key == pg.K_RALT:
		ship1.shoot = False
	elif event.key == pg.K_UP:
		ship1.movingUp = False
	elif event.key == pg.K_DOWN:
		ship1.movingDown = False
	elif event.key == pg.K_d:
		ship2.movingRight = False
	elif event.key == pg.K_a:
		ship2.movingLeft = False
	elif event.key == pg.K_s:
		ship2.movingDown = False
	elif event.key == pg.K_w:
		ship2.movingUp = False
	elif event.key == pg.K_LALT:
		ship2.shoot = False

def pause(stats):
	"""Pause the game when the pause button is pressed"""
	paused.play()
	stats.gameActive = False
	stats.paused = True

def checkPlayBtn(setting, screen, stats, playBtn, sel, bullets, eBullets, ship1, ship2):
	"""Start new game if playbutton is pressed"""
	if not stats.gameActive and not stats.paused:
		setting.initDynamicSettings()
		stats.resetStats()
		stats.gameActive = True

		#Reset the ship and the bullets
		bullets.empty()
		eBullets.empty()
		ship1.centerShip()

	elif not stats.gameActive and stats.paused:
		#IF the game is not running and game is paused unpause the game
		stats.gameActive = True
		stats.paused = False

def updateBullets(setting, screen, stats, ship1, ship2, bullets, eBullets):
	bullets.update()

def updateScreen(setting, screen, stats, bullets, eBullets, playBtn, menuBtn, quitBtn, sel, ship1, ship2):
	"""Update images on the screen and flip to the new screen"""
	#Redraw the screen during each pass through the loop
	#Fill the screen with background color
	#Readjust the quit menu btn position
	playBtn.rect.y = 200
	playBtn.msgImageRect.y = 200
	quitBtn.rect.y = 300
	quitBtn.msgImageRect.y = 300
	menuBtn.rect.y = 250
	menuBtn.msgImageRect.y = 250
	screen.fill(setting.bgColor)
	#screen.blit(setting.bg, (0,0))

	#draw all the bullets
	for bullet in bullets.sprites():
		bullet.drawBullet()

	#draw all the enemy bullets
	for ebull in eBullets.sprites():
		ebull.drawBullet()

	ship1.blitme()
	ship2.blitme()
	#Draw the play button if the game is inActive
	if not stats.gameActive:
		playBtn.drawBtn()
		menuBtn.drawBtn()
		quitBtn.drawBtn()
		sel.blitme()
	#Make the most recently drawn screen visable.
	pg.display.flip()