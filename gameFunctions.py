import random
import sys
import time
import pygame as pg
import sounds
from time import sleep
from alien import Alien
from bullet import Bullet, SpecialBullet
from item import Item

clock = pg.time.Clock()
FPS = 120
reset = 0

gameOverButtons = ["retry", "menu", "quit"]
pauseButtons = ["play", "menu", "quit"]


def checkEvents(setting, screen, stats, sb, bMenu, ship, aliens, bullets, eBullets, charged_bullets):
    """Respond to keypresses and mouse events."""
    for event in pg.event.get():
        # Check for quit event
        if event.type == pg.QUIT:
            sys.exit()

            # Check for key down has been pressed
        elif event.type == pg.KEYDOWN:
            checkKeydownEvents(event, setting, screen, stats, sb, ship, aliens, bullets, eBullets)
            if (stats.gameActive):
                continue
            if event.key == pg.K_UP:
                sounds.control_menu.play()
                bMenu.up()
            elif event.key == pg.K_DOWN:
                sounds.control_menu.play()
                bMenu.down()
            elif event.key == pg.K_RETURN:
                sounds.select_menu.play()
                selectedName, selectedBtn = bMenu.getSelectedButton()
                if selectedBtn:
                    #######################
                    buttonAction(stats, selectedName, setting, screen, ship, aliens, bullets, eBullets)
        elif event.type == pg.KEYUP:
            checkKeyupEvents(event, setting, screen, stats, ship, bullets, charged_bullets)

        elif event.type == pg.MOUSEMOTION:
            if not stats.gameActive:
                mouseBtnName, mouseBtn = bMenu.mouseCheck(event.pos[0], event.pos[1])
                if mouseBtn is not None:
                    selectedName, selectedBtn = bMenu.getSelectedButton()
                    if mouseBtn is not selectedBtn:
                        sounds.control_menu.play()
                        bMenu.selectByName(mouseBtnName)

        elif event.type == pg.MOUSEBUTTONDOWN:
            if not stats.gameActive:
                pressed = pg.mouse.get_pressed()
                if (pressed[0]):
                    pos = pg.mouse.get_pos()
                    mouseBtnName, mouseBtn = bMenu.mouseCheck(pos[0], pos[1])
                    if mouseBtn is not None:
                        sounds.select_menu.play()
                        buttonAction(stats, mouseBtnName, setting, screen, ship, aliens, bullets, eBullets)


def buttonAction(stats, selectedName, setting, screen, ship, aliens, bullets, eBullets):
    if selectedName in ('play', 'retry'):
        checkPlayBtn(setting, screen, stats, ship, aliens, bullets, eBullets)
    elif selectedName == 'menu':
        stats.setGameLoop('mainMenu')
        stats.resetStats()
    elif selectedName == 'quit':
        pg.time.delay(300)
        sys.exit()


def checkKeydownEvents(event, setting, screen, stats, sb, ship, aliens, bullets, eBullets):
    """Response to kepresses"""
    if event.key == pg.K_RIGHT:
        # Move the ship right
        ship.movingRight = True
    elif event.key == pg.K_LEFT:
        # Move the ship left
        ship.movingLeft = True
    elif event.key == pg.K_UP:
        # Move the ship up
        ship.movingUp = True
    elif event.key == pg.K_DOWN:
        # Move the ship down
        ship.movingDown = True
    elif event.key == pg.K_TAB:
        # Change the style of trajectory of bullet
        if (ship.trajectory < 4):
            ship.trajectory += 1
        else:
            ship.trajectory = 0
    elif event.key == pg.K_SPACE:
        if not stats.paused:
            if ship.checkReadyToShoot() and (len(bullets) < 10):
                sounds.attack.play()
                newBullet = Bullet(setting, screen, ship, ship.trajectory)
                bullets.add(newBullet)
                ship.setNextShootTime()
            ship.chargeGaugeStartTime = pg.time.get_ticks()
            ship.shoot = True

    elif event.key == pg.K_x or event.key == 167:
        # Ultimate key
        useUltimate(setting, screen, stats, bullets, stats.ultimatePattern)
        # Check for pause key
    elif event.key == pg.K_p or event.key == 181:
        sounds.paused.play()
        pause(stats)
        # Add speed control key
    elif event.key == pg.K_q or event.key == 172:
        setting.halfspeed()
    elif event.key == pg.K_w or event.key == 173:
        setting.doublespeed()
    elif event.key == pg.K_c or event.key == 168:
        # interception Key
        setting.checkBtnPressed += 1
        if setting.checkBtnPressed % 2 != 0:
            setting.interception = True
        else:
            setting.interception = False
    elif event.key == pg.K_F12:
        # Reset Game
        sounds.button_click_sound.play()
        resetGame()
    elif event.key == pg.K_ESCAPE:
        # Quit game
        sounds.button_click_sound.play()
        pg.time.delay(300)
        sys.exit()


def checkKeyupEvents(event, setting, screen, stats, ship, bullets, charged_bullets):
    """Response to keyrealeses"""
    global gauge
    if event.key == pg.K_RIGHT:
        ship.movingRight = False
    elif event.key == pg.K_LEFT:
        ship.movingLeft = False
    elif event.key == pg.K_UP:
        ship.movingUp = False
    elif event.key == pg.K_DOWN:
        ship.movingDown = False
    elif event.key == pg.K_SPACE:
        if not stats.paused:
            if (ship.chargeGauge == 100):
                sounds.charge_shot.play()
                newBullet = Bullet(setting, screen, ship, ship.trajectory, 3, 5)
                bullets.add(newBullet)
                ship.chargeGauge = 0
            elif (50 <= ship.chargeGauge):
                sounds.charge_shot.play()
                newBullet = Bullet(setting, screen, ship, ship.trajectory, 2, 3)
                charged_bullets.add(newBullet)
        ship.shoot = False


def pause(stats):
    """Pause the game when the pause button is pressed"""
    stats.gameActive = False
    stats.paused = True


def resetGame():
    global reset
    reset = 1
    stats.highScore = 0
    stats.saveHighScore()


def checkPlayBtn(setting, screen, stats, ship, aliens, bullets, eBullets):
    """Start new game if playbutton is pressed"""
    if not stats.gameActive and not stats.paused:
        setting.initDynamicSettings()
        stats.resetStats()
        stats.gameActive = True

        # Reset the alien and the bullets
        aliens.empty()
        bullets.empty()
        eBullets.empty()

        # Create a new fleet and center the ship
        createFleet(setting, stats, screen, ship, aliens)
        ship.centerShip()

    elif not stats.gameActive and stats.paused:
        # IF the game is not running and game is paused unpause the game
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


def createAlien(setting, stats, screen, aliens, alienNumber, rowNumber):
    sounds.stage_clear.play()
    if setting.gameLevel == "normal":
        alien = Alien(setting, screen, 1 + stats.level // 4)
    else:
        alien = Alien(setting, screen, 1 + stats.level // 2)        
    alienWidth = alien.rect.width
    screenRect = alien.screen.get_rect()
    alien.x = alienWidth + 2 * alienWidth * alienNumber
    """ random position of enemy will be created in game window"""
    alien.rect.x = random.randrange(0, setting.screenWidth - alien.x / 2)
    alien.rect.y = (alien.rect.height + random.randrange(0, setting.screenHeight - alien.rect.height * 2)) / 1.5
    aliens.add(alien)

def createBoss(setting, stats, screen, aliens, alienNumber, rowNumber):
    sounds.stage_clear.play()
    alien = Alien(setting, screen, stats.level*30, True)
    alienWidth = alien.rect.width
    screenRect = alien.screen.get_rect()
    alien.x = alienWidth + 2 * alienWidth * alienNumber
    """ random position of enemy will be created in game window"""
    alien.rect.x = setting.screenWidth / 2
    alien.rect.y = 30
    aliens.add(alien)

def createItem(setting, screen, posx, posy, type, items):
    """add item func"""
    # item number is 1 per type
    for itype in items:
        if itype.type == type:
            return
    item = Item(setting, screen, type, posx, posy)
    screenRect = item.screen.get_rect()
    items.add(item)


def createFleet(setting, stats, screen, ship, aliens):
    """Create a fleet of aliens"""
    alien = Alien(setting, screen, stats.level*3)
    numberAliensX = getNumberAliens(setting, alien.rect.width)
    numberRows = getNumberRows(setting, ship.rect.height, alien.rect.height)

    # create the first row of aliens
    for rowNumber in range(numberRows):
        for alienNumber in range(numberAliensX):
            createAlien(setting, stats, screen, aliens, alienNumber, rowNumber)


def createFleetBoss(setting, stats, screen, ship, aliens):
    """Create a fleet of aliens"""
    alien = Alien(setting, screen, stats.level*3)
    numberAliensX = 1
    numberRows = 1

    # create the first row of aliens
    createBoss(setting, stats, screen, aliens, numberAliensX, numberRows)
            
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
        ##############
        if setting.gameLevel == 'normal':
            alien.rect.y += setting.fleetDropSpeed
        elif setting.gameLevel == 'hard':
            alien.rect.y += (setting.fleetDropSpeed + 3)
    setting.fleetDir *= -1


def shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
    """Respond to ship being hit"""
    if stats.shipsLeft > 0:
        if pg.time.get_ticks() - setting.newStartTime > setting.invincibileTime:
            sounds.explosion_sound.play()
            stats.shipsLeft -= 1
            stats.ultimateGauge = 0
            ship.chargeGauge = 0
            ship.chargeGaugeStartTime = pg.time.get_ticks()
            # ship.centerShip()
            setting.newStartTime = pg.time.get_ticks()
    elif stats.shipsLeft == 0:
        if pg.time.get_ticks() - setting.newStartTime > setting.invincibileTime:
            sounds.explosion_sound.play()
            stats.ultimateGauge = 0
            ship.chargeGauge = 0
            ship.chargeGaugeStartTime = pg.time.get_ticks()
            setting.newStartTime = pg.time.get_ticks()
            stats.gameActive = False
            checkHighScore(stats, sb)
    else:
        stats.gameActive = False
        checkHighScore(stats, sb)

def updateInvincibility(setting, screen, ship):
    if pg.time.get_ticks() - setting.newStartTime < setting.invincibileTime:
        text1 = pg.font.Font('Fonts/Square.ttf', 20).render("SHIELD", True, (255, 255, 255), )
        screen.blit(text1, (ship.rect.x, ship.rect.y -20))

def updateAliens(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
    """Update the aliens"""
    checkFleetEdges(setting, aliens)
    checkFleetBottom(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
    aliens.update(setting, screen, ship, aliens, eBullets)

    #look for alien-ship collision
    if pg.sprite.spritecollideany(ship, aliens):
        #74
        shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
        #sb.prepShips()


def updateBullets(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, items):
    """update the position of the bullets"""
    #check if we are colliding
    bullets.update()
    for eBullet in eBullets:
        eBullet.update()
    charged_bullets.update()
    checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, items)
    checkEBulletShipCol(setting, stats, sb, screen, ship, aliens, bullets, eBullets)

    #if bullet goes off screen delete it
    for bullet in eBullets.copy():
        screenRect = screen.get_rect()
        if bullet.rect.top >= screenRect.bottom:
            eBullets.remove(bullet)
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for charged_bullet in charged_bullets.copy():
        if charged_bullet.rect.bottom <= 0:
            charged_bullets.remove(charged_bullet)

    if setting.interception:
        pg.sprite.groupcollide(bullets, eBullets, bullets, eBullets)


def updateItems(setting, screen, stats, sb, ship, aliens, bullets, eBullets, items):
    """update the position of the bullets"""
    #check if we are colliding
    items.update()
    #if bullet goes off screen delete it
    for item in items.sprites():
        screenRect = screen.get_rect()
        if item.rect.top >= screenRect.bottom:
            items.remove(item)
    for item in items.sprites():
        if item.rect.bottom <= 0:
            items.remove(item)
    for item in items.sprites():
        if item.rect.centerx -30 < ship.rect.x < item.rect.x +30 and item.rect.centery -20 < ship.rect.centery < item.rect.centery +20:
            if item.type == 1:
                if stats.shipsLeft < setting.shipLimit:
                    stats.shipsLeft += 1
                else:
                    stats.score += setting.alienPoints * 3
            items.remove(item)


def checkBulletAlienCol(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, items):
    """Detect collisions between alien and bullets"""
    collisions = pg.sprite.groupcollide(aliens, bullets, False, False)
    collisions.update(pg.sprite.groupcollide(aliens, charged_bullets, False, False))
    if collisions:
        sounds.enemy_explosion_sound.play()

        for alien in collisions :
            #charged_bullet bgManager
            for charged_bullet in charged_bullets:
                alien.hitPoint -= charged_bullet.damage
            for bullet in collisions[alien] :
                alien.hitPoint -= bullet.damage
                bullets.remove(bullet)
            if alien.hitPoint <= 0 :
                setting.explosions.add(alien.rect.x, alien.rect.y)
                sounds.enemy_explosion_sound.play()
                #if an enemy dies, it falls down an item randomly.
                i = random.randrange(100)
                if i<=setting.probabilityHeal:
                    createItem(setting, screen, alien.rect.x, alien.rect.y, 1, items)
                aliens.remove(alien)

        # Increase the ultimate gauge, upto 100
        if not collisions[alien][0].isUltimate:
            if setting.gameLevel == 'normal':
                stats.ultimateGauge += setting.ultimateGaugeIncrement   # ultimateGaugeIncrement = 3
            elif setting.gameLevel == 'hard':
                stats.ultimateGauge += 1
        if stats.ultimateGauge > 100:
            stats.ultimateGauge = 100
        for aliens in collisions.values():
            stats.score += setting.alienPoints * len(aliens)
        checkHighScore(stats, sb)


    sb.prepScore()
    #Check if there are no more aliens
    if len(aliens) == 0:
        # Destroy exsiting bullets and create new fleet
        sounds.stage_clear.play()
        bullets.empty()
        eBullets.empty()
        setting.increaseSpeed() #Speed up game
        stats.level += 1
        setting.setIncreaseScoreSpeed(stats.level)
        sb.prepLevel()
        if stats.level % 5 != 0:
            createFleet(setting, stats, screen, ship, aliens)
        else:
            createFleetBoss(setting, stats, screen, ship, aliens)
        # Invincibility during 2 sec
        setting.newStartTime = pg.time.get_ticks()


def checkEBulletShipCol(setting, stats, sb, screen, ship, aliens, bullets, eBullets):
    """Check for collisions using collision mask between ship and enemy bullets"""
    for ebullet in eBullets.sprites():
        if pg.sprite.collide_mask(ship, ebullet):
            shipHit(setting, stats, sb, screen, ship, aliens, bullets, eBullets)
            #sb.prepShips()
            eBullets.remove(ebullet)


def checkHighScore(stats, sb):
    """Check to see if high score has been broken"""
    if stats.score > stats.highScore:
        stats.highScore = stats.score
        stats.saveHighScore()


def updateUltimateGauge(setting, screen, stats, sb):
    """Draw a bar that indicates the ultimate gauge"""
    x = sb.levelRect.left - 130
    y = sb.levelRect.top + 4
    gauge = stats.ultimateGauge
    ultimateImg = pg.font.Font('Fonts/Square.ttf', 10).render("POWER SHOT(X)", True, (255, 255, 255),
                                                              (255, 100, 0))
    ultimateRect = ultimateImg.get_rect()
    ultimateRect.x = x + 5
    ultimateRect.y = y
    if gauge == 100:
        pg.draw.rect(screen, (255, 255, 255), (x, y, 100, 12), 0)
        pg.draw.rect(screen, (255, 100, 0), (x, y, gauge, 12), 0)
        screen.blit(ultimateImg, ultimateRect)
    else:
        pg.draw.rect(screen, (255, 255, 255), (x, y, 100, 12), 0)
        pg.draw.rect(screen, (0, 255, 255), (x, y, gauge, 12), 0)


def UltimateDiamondShape(setting, screen, stats, sbullets):
    xpos = 10
    yCenter = setting.screenHeight + (setting.screenWidth / 50) * 20
    yGap = 0
    # Make a diamond pattern
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
        sounds.ult_attack.play()
        UltimateDiamondShape(setting, screen, stats, sbullets)
    # elif pattern == 2:
    #		make other pattern
    stats.ultimateGauge = 0


def updateChargeGauge(ship):
    gauge = 0
    if ship.shoot == True:
        gauge = 100 * ((pg.time.get_ticks() - ship.chargeGaugeStartTime) / ship.fullChargeTime)
        if (100 < gauge):
            gauge = 100
    ship.chargeGauge = gauge


def drawChargeGauge(setting, screen, ship, sb):
    x = sb.levelRect.left - 240
    y = sb.levelRect.top + 4
    color = (50, 50, 50)
    if (ship.chargeGauge == 100):
        color = (255, 0, 0)
    elif (50 <= ship.chargeGauge):
        color = (255, 120, 0)

    pg.draw.rect(screen, (255, 255, 255), (x, y, 100, 10), 0)
    pg.draw.rect(screen, color, (x, y, ship.chargeGauge, 10), 0)


def updateScreen(setting, screen, stats, sb, ship, aliens, bullets, eBullets, charged_bullets, bMenu, bgManager, items):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    # Fill the screen with background color
    # Readjust the quit menu btn position
    global clock, FPS, gameOverButtons, pauseButtons
    bMenu.drawMenu()
    bgManager.update()
    bgManager.draw()



    # draw all the bullets
    for bullet in bullets.sprites():
        bullet.drawBullet()

    # draw all the enemy bullets
    for ebull in eBullets.sprites():
        ebull.drawBullet()

    for charged_bullet in charged_bullets.sprites():
        charged_bullet.drawBullet()

    ship.blitme()
    aliens.draw(screen)

    for i in items:
        i.update()
        i.drawitem()
    #Shield if ship is invincibile
    updateInvincibility(setting, screen, ship)

    # Update Ultimate Gauge
    updateUltimateGauge(setting, screen, stats, sb)

    # Update and draw Charge Gauge
    updateChargeGauge(ship)
    drawChargeGauge(setting, screen, ship, sb)

    # Draw the scoreboard
    sb.prepScore()
    sb.prepHighScore()
    sb.prepLevel()
    sb.showScore()

    # Draw the play button if the game is inActive
    if not stats.gameActive:
        if (stats.shipsLeft < 1):
            bMenu.setMenuButtons(gameOverButtons)
            scoreImg = pg.font.Font('Fonts/Square.ttf', 50).render("Score: " + str(stats.score), True, (0, 0, 0),
                                                                   (255, 255, 255))
            screen.fill((0, 0, 0))
            screen.blit(scoreImg, ((setting.screenWidth - scoreImg.get_width()) / 2, 120))
            screen.blit(setting.gameOverImage, (20, 30))
        else:
            bMenu.setMenuButtons(pauseButtons)
        bMenu.drawMenu()
    setting.explosions.draw(screen)
    # Make the most recently drawn screen visable.
    pg.display.update()
    clock.tick(FPS)
