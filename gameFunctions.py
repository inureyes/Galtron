import sys
import pygame as pg
from time import sleep
from bullet import Bullet
from alien import Alien

pauseBtnState = 1
back = False

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
	elif event.key == pg.K_SPACE:
		newBullet = Bullet(setting, screen, ship)
		bullets.add(newBullet)
	#Check for pause key
	elif event.key == pg.K_p:
		pause(stats)
	elif event.key == pg.K_ESCAPE:
		#Quit game
		sys.exit()

def checkKeyupEvents(event, ship):
	"""Response to keyrealeses"""
	if event.key == pg.K_RIGHT:
		ship.movingRight = False
	elif event.key == pg.K_LEFT:
		ship.movingLeft = False


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
	numberRows = int(availableSpaceY / (2 * alienHeight))
	return numberRows


def createAlien(setting, screen, aliens, alienNumber, rowNumber):
	alien = Alien(setting, screen)
	alienWidth = alien.rect.width
	alien.x = alienWidth + 2 * alienWidth * alienNumber
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * rowNumber
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
		#Empty teh list of aliens and bullets
		aliens.empty()
		bullets.empty()
		eBullets.empty()
		#Create a new fleet and center the ship.
		createFleet(setting, screen, ship, aliens)
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
	aliens.update(setting, screen, ship, aliens, eBullets)

	#look for alien-ship collision
	if pg.sprite.spritecollideany(ship, aliens):
		shipHit(setting, stats, sb, screen, ship, aliens, bullets)
		sb.prepShips()


def updateBullets(setting, screen, stats, sb, ship, aliens, bullets, eBullets):
	"""update the position of the bullets"""
	#check if we are colliding
	bullets.update()
	eBullets.update()
	checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets)
	checkEBulletShipCol(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
	#if bullet goes off screen delete it
	for bullet in eBullets.copy():
		screenRect = screen.get_rect()
		if bullet.rect.top >= screenRect.bottom:
			eBullets.remove(bullet)
	for bullet in bullets.copy(): 
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	

def checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets):
	"""Detect collisions between alien and bullets"""
	collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += setting.alienPoints * len(aliens)
		checkHighScore(stats, sb)
	sb.prepScore()
	#Check if there are no more aliens
	if len(aliens) == 0:
		#Destroy exsiting bullets and create new fleet
		bullets.empty()
		setting.increaseSpeed() #Speed up game
		stats.level += 1
		sb.prepLevel()
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


def updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, playBtn, menuBtn, quitBtn, sel):
	"""Update images on the screen and flip to the new screen"""
	#Redraw the screen during each pass through the loop
	#Fill the screen with background color
	#Readjust the quit menu btn position
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

	ship.blitme()
	aliens.draw(screen)

	#Draw the scoreboard
	sb.showScore()

	#Draw the play button if the game is inActive
	if not stats.gameActive:
		playBtn.drawBtn()
		menuBtn.drawBtn()
		quitBtn.drawBtn()
		sel.blitme()
	#Make the most recently drawn screen visable.
	pg.display.flip()