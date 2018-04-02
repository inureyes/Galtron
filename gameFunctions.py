import sys, time
import pygame as pg
from time import sleep
from bullet import Bullet, SpecialBullet
from alien import Alien
from settings import Settings
import random


pauseBtnState = 1
back = False

x = 0
clock = pg.time.Clock()
FPS = 120
def checkEvents(setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets, eBullets):
	"""Respond to keypresses and mouse events."""
	global pauseBtnState
	for event in pg.event.get():
		#Check for quit event
		if event.type == pg.QUIT:
			sys.exit()

		#Check for key down has been pressed
		elif event.type == pg.KEYDOWN:
			checkKeydownEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets, eBullets, pauseBtnState)
			#Pause menu controls
			if event.key == pg.K_UP:
				if pauseBtnState > 1:
					pauseBtnState -= 1
					sel.rect.y -= 50
			elif event.key == pg.K_DOWN:
				if pauseBtnState < 3:
					pauseBtnState += 1
					sel.rect.y += 50

			elif event.key == pg.K_RETURN:
				if pauseBtnState == 1:
					checkPlayBtn(setting, screen, stats, sb, playBtn, sel, ship, aliens, bullets, eBullets)
				elif pauseBtnState == 2:
					stats.mainGame = False
					stats.mainAbout = False
					stats.twoPlay = False
					stats.mainMenu = True
					sel.rect.centery = playBtn.rect.centery
					pauseBtnState = 1
				elif pauseBtnState == 3:
					sys.exit()

		#Check if the key has been released
		elif event.type == pg.KEYUP:
			checkKeyupEvents(event, ship)


def checkKeydownEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship, aliens, bullets, eBullets, pauseBtnState):
	"""Response to kepresses"""
	global back
	if event.key == pg.K_RIGHT:
		#Move the ship right
		ship.movingRight = True
	elif event.key == pg.K_LEFT:
		#Move the ship left
		ship.movingLeft = True
	elif event.key == pg.K_UP:
		#Move the ship up
		ship.movingUp = True
	elif event.key == pg.K_DOWN:
		#Move the ship down
		ship.movingDown = True
	elif event.key == pg.K_TAB:
		#Change the style of trajectory of bullet
		if (ship.trajectory < 5):
			ship.trajectory += 1
		else:
			ship.trajectory = 0
	elif event.key == pg.K_SPACE:
		if len(bullets) <= 6:
			newBullet = Bullet(setting, screen, ship, ship.trajectory)
			bullets.add(newBullet)
		ship.shoot = True
	elif event.key == pg.K_x:
		#Ultimate key
		useUltimate(setting, screen, stats, bullets, stats.ultimatePattern)
	#Check for pause key
	elif event.key == pg.K_p:
		pause(stats)
	#Add speed control key
	elif event.key == pg.K_q:
		setting.halfspeed()
	elif event.key == pg.K_w:
		setting.doublespeed()
	elif event.key == pg.K_ESCAPE:
		#Quit game
		sys.exit()

def checkKeyupEvents(event, ship):
	"""Response to keyrealeses"""
	if event.key == pg.K_RIGHT:
		ship.movingRight = False
	elif event.key == pg.K_LEFT:
		ship.movingLeft = False
	elif event.key == pg.K_UP:
		ship.movingUp = False
	elif event.key == pg.K_DOWN:
		ship.movingDown = False
	elif event.key == pg.K_SPACE:
		ship.shoot = False

def pause(stats):
	"""Pause the game when the pause button is pressed"""
	stats.gameActive = False
	stats.paused = True


def checkPlayBtn(setting, screen, stats, sb, playBtn, sel, ship, aliens, bullets, eBullets):
	"""Start new game if playbutton is pressed"""
	if not stats.gameActive and not stats.paused:
		setting.initDynamicSettings()
		stats.resetStats()
		stats.gameActive = True

		#Reset the alien and the bullets
		aliens.empty()
		bullets.empty()
		eBullets.empty()

		#Create a new fleet and center the ship
		createFleet(setting, screen, ship, aliens)
		ship.centerShip()

		#Reset score and level
		sb.prepShips()
		sb.prepScore()
		sb.prepLevel()
		sb.prepHighScore()

	elif not stats.gameActive and stats.paused:
		#IF the game is not running and game is paused unpause the game
		stats.gameActive = True
		stats.paused = False



def getNumberAliens(setting, alienWidth):
	"""Determine the number of aliens that fit in a row"""
	availableSpaceX = setting.screenWidth - 2 * alienWidth
	numberAliensX = int(availableSpaceX / (2 * alienWidth))
	return numberAliensX


def getNumberRows(setting, shipHeight, alienHeight):
	"""Determine the number of rows of aliens that fit on the screen"""
	availableSpaceY = (setting.screenHeight - (3 * alienHeight) - shipHeight)
	numberRows = int(availableSpaceY / (3 * alienHeight))
	return numberRows


def createAlien(setting, screen, aliens, alienNumber, rowNumber):
	alien = Alien(setting, screen)
	alienWidth = alien.rect.width
	screenRect = alien.screen.get_rect()
	alien.x = alienWidth + 2 * alienWidth * alienNumber
	""" random position of enemy will be created in game window"""
	alien.rect.x =  random.randrange(0,setting.screenWidth-alien.x/2)
	alien.rect.y = (alien.rect.height + random.randrange(0,setting.screenHeight-alien.rect.height*2))/1.5
	aliens.add(alien)


def createFleet(setting, screen, ship, aliens):
	"""Create a fleet of aliens"""
	alien = Alien(setting, screen)
	numberAliensX = getNumberAliens(setting, alien.rect.width)
	numberRows = getNumberRows(setting, ship.rect.height, alien.rect.height)

	#create the first row of aliens
	for rowNumber in range(numberRows):
		for alienNumber in range(numberAliensX):
			createAlien(setting, screen, aliens, alienNumber, rowNumber)



def checkFleetEdges(setting, aliens):
	"""Respond if any aliens have reached an edge"""
	for alien in aliens.sprites():
		if alien.checkEdges():
			changeFleetDir(setting, aliens)
			break

def checkFleetBottom(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
	"""Respond if any aliens have reached an bottom of screen"""
	for alien in aliens.sprites():
		if alien.checkBottom():
			shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets)


def changeFleetDir(setting, aliens):
	"""Change the direction of aliens"""
	for alien in aliens.sprites():
		alien.rect.y += setting.fleetDropSpeed
	setting.fleetDir *= -1


def shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
	"""Respond to ship being hit"""
	if stats.shipsLeft > 0:
		sb.prepShips()
		stats.shipsLeft -= 1
		stats.ultimateGauge = 0
		#Empty the list of aliens and bullets
#		aliens.empty()
#		bullets.empty()
#		eBullets.empty()
		#Create a new fleet and center the ship.
#		createFleet(setting, screen, ship, aliens)
		ship.centerShip()
		sb.prepShips()
		sb.prepScore()
		sleep(0.5)
	else:
		stats.gameActive = False
		checkHighScore(stats, sb)


def updateAliens(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
	"""Update the aliens"""
	checkFleetEdges(setting, aliens)
	checkFleetBottom(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
	aliens.update(setting, screen, ship, aliens, eBullets)

	#look for alien-ship collision
	if pg.sprite.spritecollideany(ship, aliens):
		#74
		shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
		sb.prepShips()


def updateBullets(setting, screen, stats, sb, ship, aliens, bullets, eBullets):
	"""update the position of the bullets"""
	#check if we are colliding
	bullets.update()
	eBullets.update()
	checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets, eBullets)
	checkEBulletShipCol(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
	#if bullet goes off screen delete it
	for bullet in eBullets.copy():
		screenRect = screen.get_rect()
		if bullet.rect.top >= screenRect.bottom:
			eBullets.remove(bullet)
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
      


def checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets, eBullets):
	"""Detect collisions between alien and bullets"""
	collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for c in collisions:
			setting.explosions.add(c.rect.x, c.rect.y)

		#Increase the ultimate gauge, upto 100
		stats.ultimateGauge += setting.ultimateGaugeIncrement
		if stats.ultimateGauge > 100:
			stats.ultimateGauge = 100
		for aliens in collisions.values():
			stats.score += setting.alienPoints * len(aliens)
		checkHighScore(stats, sb)
	sb.prepScore()
	#Check if there are no more aliens
	if len(aliens) == 0:
		#Destroy exsiting bullets and create new fleet
		bullets.empty()
		eBullets.empty()
		setting.increaseSpeed() #Speed up game
		stats.level += 1
		sb.prepLevel()
		time.sleep(1)
		createFleet(setting, screen, ship, aliens)

def checkEBulletShipCol(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
	"""Check for collisions using collision mask between ship and enemy bullets"""
	for ebullet in eBullets.sprites():
		if pg.sprite.collide_mask(ship, ebullet):
			shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
			sb.prepShips()


def checkHighScore(stats, sb):
	"""Check to see if high score has been broken"""
	if stats.score > stats.highScore:
		stats.highScore = stats.score
		sb.prepHighScore()

def updateUltimateGauge(setting, screen, stats):
	"""Draw a bar that indicates the ultimate gauge"""
	x = 290
	y = 15
	gauge = stats.ultimateGauge
	pg.draw.rect(screen, (255,255,255), (x,y,100,10), 0)
	pg.draw.rect(screen, (0,0,255), (x,y,gauge,10), 0)

def UltimateDiamondShape(setting, screen, stats, sbullets):
	xpos = 10
	yCenter = setting.screenHeight + (setting.screenWidth / 50) * 20
	yGap = 0
	#Make a diamond pattern
	while xpos <= setting.screenWidth:
		if yGap == 0:
			sBullet = SpecialBullet(setting, screen, (xpos, yCenter))
			sbullets.add(sBullet)
		else:
			upBullet = SpecialBullet(setting, screen, (xpos, yCenter + yGap))
			downBullet = SpecialBullet(setting, screen, (xpos, yCenter - yGap))
			sbullets.add(upBullet)
			sbullets.add(downBullet)
		if xpos <= setting.screenWidth / 2:
			yGap += 20
		else:
			yGap -= 20
		xpos += setting.screenWidth / 30

def useUltimate(setting, screen, stats, sbullets, pattern):
	if stats.ultimateGauge != 100:
		return
	if pattern == 1:
		UltimateDiamondShape(setting, screen, stats, sbullets)
#	elif pattern == 2:
#		make other pattern
	stats.ultimateGauge = 0





def updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, playBtn, menuBtn, quitBtn, sel):
	"""Update images on the screen and flip to the new screen"""
	#Redraw the screen during each pass through the loop
	#Fill the screen with background color
	#Readjust the quit menu btn position
	global x, clock, FPS
	quitBtn.rect.y = 300
	quitBtn.msgImageRect.y = 300
	menuBtn.rect.y = 250
	menuBtn.msgImageRect.y = 250
	#screen.fill(setting.bgColor)
	rel_x = x % setting.bg.get_rect().height
	screen.blit(setting.bg, (0,rel_x - setting.bg.get_rect().height))
	if rel_x < setting.screenHeight:
		screen.blit(setting.bg, (0,rel_x))
	x += 3

	#draw all the bullets
	for bullet in bullets.sprites():
		bullet.drawBullet()

	#draw all the enemy bullets
	for ebull in eBullets.sprites():
		ebull.drawBullet()

	ship.blitme()
	aliens.draw(screen)

	#Update Ultimate Gauge
	updateUltimateGauge(setting, screen, stats)

	#Draw the scoreboard
	sb.showScore()

	#Draw the play button if the game is inActive
	if not stats.gameActive:
		playBtn.drawBtn()
		menuBtn.drawBtn()
		quitBtn.drawBtn()
		sel.blitme()
	setting.explosions.draw(screen)
	#Make the most recently drawn screen visable.
	pg.display.flip()
	pg.display.update()
	clock.tick(FPS)

