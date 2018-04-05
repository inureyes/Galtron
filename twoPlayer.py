import random
import sys
import time
from time import sleep

import pygame as pg

# from bullet import Bullet
import sounds
from alien import Alien
from bullet import Bullet, SpecialBullet

pauseBtnState2 = 1
back = False

x = 0
clock = pg.time.Clock()
FPS = 120
bgloop = 0
reset = 0


def checkEvents(setting, screen, stats, sb, playBtn, quitBtn, sel, bullets, aliens, eBullets, ship1, ship2):
    """Respond to keypresses and mouse events."""
    global pauseBtnState2
    for event in pg.event.get():
        # Check for quit event
        if event.type == pg.QUIT:
            sys.exit()

            # Check for key down has been pressed
        elif event.type == pg.KEYDOWN:
            checkKeydownEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship1, ship2, aliens, bullets,
                               eBullets, pauseBtnState2)
            if (stats.gameActive):
                continue
            if event.key == pg.K_UP:
                if pauseBtnState2 > 1:
                    sounds.control_menu.play()
                    pauseBtnState2 -= 1
                    sel.rect.y -= 50
            elif event.key == pg.K_DOWN:
                if pauseBtnState2 < 3:
                    sounds.control_menu.play()
                    pauseBtnState2 += 1
                    sel.rect.y += 50

            elif event.key == pg.K_RETURN:
                if pauseBtnState2 == 1:
                    sounds.select_menu.play()

                    checkPlayBtn(setting, screen, stats, sb, playBtn, sel, ship1, ship2, aliens, bullets, eBullets)
                elif pauseBtnState2 == 2:
                    sounds.select_menu.play()
                    stats.twoPlay = False
                    stats.mainMenu = True
                    stats.resetStats()
                    sel.rect.centery = playBtn.rect.centery
                    pauseBtnState2 = 1
                elif pauseBtnState2 == 3:
                    sounds.button_click_sound.play()
                    pg.time.delay(300)
                    sys.exit()
                    # Check if the key has been released
        elif event.type == pg.KEYUP:
            checkKeyupEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship1, ship2, aliens, bullets,
                             eBullets, pauseBtnState2)
            # elif event.type == pg.MOUSEMOTION:
        #	ship1.center = event.pos[0]
        #	ship1.centery = event.pos[1]
        #	ship2.center = event.pos[0]
        #	ship2.centery = event.pos[1]


def checkKeydownEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship1, ship2, aliens, bullets,
                       eBullets, pauseBtnState2):
    """Response to kepresses"""
    global back
    # Movement of the ship1

    if event.key == pg.K_RIGHT:
        ship1.movingRight = True
    elif event.key == pg.K_LEFT:
        ship1.movingLeft = True
    elif event.key == pg.K_UP:
        ship1.movingUp = True
    elif event.key == pg.K_DOWN:
        ship1.movingDown = True
    elif event.key == pg.K_RALT:
        # sounds.attack.play()
        # ship1.shoot = True
        if not stats.paused:
            if len(bullets) < 10:
                sounds.attack.play()
                newBullet = Bullet(setting, screen, ship1, ship1.trajectory)
                bullets.add(newBullet)
                ship1.chargeGaugeStartTime = pg.time.get_ticks()
                ship1.shoot = True
    elif event.key == pg.K_RSHIFT:
        # Change the style of trajectory of bullet
        if (ship1.trajectory < 5):
            ship1.trajectory += 1
        else:
            ship1.trajectory = 0
            # Movement of the ship2
    elif event.key == pg.K_d:
        ship2.movingRight = True
    elif event.key == pg.K_a:
        ship2.movingLeft = True
    elif event.key == pg.K_s:
        ship2.movingDown = True
    elif event.key == pg.K_w:
        ship2.movingUp = True
    elif event.key == pg.K_LALT:
        # sounds.attack.play()
        # ship2.shoot = True
        if not stats.paused:
            if len(bullets) < 10:
                sounds.attack.play()
                newBullet = Bullet(setting, screen, ship2, ship2.trajectory)
                bullets.add(newBullet)
                ship2.chargeGaugeStartTime = pg.time.get_ticks()
                ship2.shoot = True

    elif event.key == pg.K_LSHIFT:
        # Change the style of trajectory of bullet
        if (ship2.trajectory < 5):
            ship2.trajectory += 1
        else:
            ship2.trajectory = 0
            # Check for pause key
    elif event.key == pg.K_p:
        sounds.paused.play()
        pause(stats)
    elif event.key == pg.K_F12:
        # Reset Game
        sounds.button_click_sound.play()
        resetGame()
    elif event.key == pg.K_ESCAPE:
        # Quit game
        sounds.button_click_sound.play()
        pg.time.delay(300)
        sys.exit()


def checkKeyupEvents(event, setting, screen, stats, sb, playBtn, quitBtn, sel, ship1, ship2, aliens, bullets, eBullets,
                     pauseBtnState2):
    """Response to keyrealeses"""
    global gauge
    if event.key == pg.K_RIGHT:
        ship1.movingRight = False
    elif event.key == pg.K_LEFT:
        ship1.movingLeft = False
    elif event.key == pg.K_UP:
        ship1.movingUp = False
    elif event.key == pg.K_DOWN:
        ship1.movingDown = False
    elif event.key == pg.K_RALT:
        if not stats.paused:
            if (ship1.chargeGauge == 100):
                sounds.charge_shot.play()
                newBullet = Bullet(setting, screen, ship1, ship1.trajectory, 2)
                bullets.add(newBullet)
                ship1.chargeGauge = 0
            elif (50 <= ship1.chargeGauge):
                sounds.charge_shot.play()
                newBullet = Bullet(setting, screen, ship1, ship1.trajectory, 1)
                bullets.add(newBullet)
        ship1.shoot = False

    elif event.key == pg.K_d:
        ship2.movingRight = False
    elif event.key == pg.K_a:
        ship2.movingLeft = False
    elif event.key == pg.K_s:
        ship2.movingDown = False
    elif event.key == pg.K_w:
        ship2.movingUp = False
    elif event.key == pg.K_LALT:
        if not stats.paused:
            if (ship2.chargeGauge == 100):
                sounds.charge_shot.play()
                newBullet = Bullet(setting, screen, ship2, ship2.trajectory, 2)
                bullets.add(newBullet)
                ship2.chargeGauge = 0
            elif (50 <= ship2.chargeGauge):
                sounds.charge_shot.play()
                newBullet = Bullet(setting, screen, ship2, ship2.trajectory, 1)
                bullets.add(newBullet)
        ship2.shoot = False


def pause(stats):
    """Pause the game when the pause button is pressed"""
    stats.gameActive = False
    stats.paused = True


def resetGame():
    global reset
    reset = 1
    with open('data-files/highscore.json', 'w') as f_obj:
        f_obj.write('0')


def checkPlayBtn(setting, screen, stats, sb, playBtn, sel, ship1, ship2, aliens, bullets, eBullets):
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
        # createFleet 함수는 단계별로 한번만 해주시면 됩니다.
        createFleet(setting, screen, ship1, aliens)
        ship1.centerShip()
        ship2.centerShip()

        # Reset score and level
        sb.prepShips()
        sb.prepScore()
        sb.prepLevel()
        sb.prepHighScore()
        # Reset BackGround
        setting.bgimg(0)
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


def createAlien(setting, screen, aliens, alienNumber, rowNumber):
    alien = Alien(setting, screen)
    alienWidth = alien.rect.width
    screenRect = alien.screen.get_rect()
    alien.x = alienWidth + 2 * alienWidth * alienNumber
    """ random position of enemy will be created in game window"""
    alien.rect.x = random.randrange(0, setting.screenWidth - alien.x / 2)
    alien.rect.y = (alien.rect.height + random.randrange(0, setting.screenHeight - alien.rect.height * 2)) / 1.5
    aliens.add(alien)


def createFleet(setting, screen, ship, aliens):
    """Create a fleet of aliens"""
    alien = Alien(setting, screen)
    numberAliensX = getNumberAliens(setting, alien.rect.width)
    numberRows = getNumberRows(setting, ship.rect.height, alien.rect.height)

    # create the first row of aliens
    for rowNumber in range(numberRows):
        for alienNumber in range(numberAliensX):
            createAlien(setting, screen, aliens, alienNumber, rowNumber)


def checkFleetEdges(setting, aliens):
    """Respond if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.checkEdges():
            changeFleetDir(setting, aliens)
            break


def checkFleetBottom(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets):
    """Respond if any aliens have reached an bottom of screen"""
    for alien in aliens.sprites():
        if alien.checkBottom():
            shipHit(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets)


def changeFleetDir(setting, aliens):
    """Change the direction of aliens"""
    for alien in aliens.sprites():
        alien.rect.y += setting.fleetDropSpeed
    setting.fleetDir *= -1


def shipHit(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets):
    """Respond to ship being hit"""
    # add exprosion_sound
    if stats.shipsLeft > 0:
        sounds.explosion_sound.play()
        sb.prepShips()
        stats.shipsLeft -= 1
        stats.ultimateGauge = 0
        # Empty the list of aliens and bullets
        #		aliens.empty()
        #		bullets.empty()
        #		eBullets.empty()
        # Create a new fleet and center the ship.
        #		createFleet(setting, screen, ship, aliens)
        ship1.centerShip()
        ship2.centerShip()
        sb.prepShips()
        sb.prepScore()
        sleep(0.5)
    else:
        stats.gameActive = False
        checkHighScore(stats, sb)
        stats.resetStats()


def updateAliens(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets):
    """Update the aliens"""
    checkFleetEdges(setting, aliens)
    checkFleetBottom(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets)
    aliens.update(setting, screen, ship1, aliens, eBullets)

    # look for alien-ship collision
    # spritecollideany는 인자 두개만 받습니다
    if pg.sprite.spritecollideany(ship1, aliens):
        # 74
        shipHit(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets)
        sb.prepShips()
        setting.explosions.add(ship1.rect.x, ship1.rect.y)
    if pg.sprite.spritecollideany(ship2, aliens):
        shipHit(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets)
        sb.prepShips()
        setting.explosions.add(ship2.rect.x, ship2.rect.y)


def updateBullets(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets):
    """update the position of the bullets"""
    # check if we are colliding
    bullets.update()
    eBullets.update()

    checkBulletAlienCol(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets)
    checkEBulletShipCol(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets)

    # if bullet goes off screen delete it
    for bullet in eBullets.copy():
        screenRect = screen.get_rect()
        if bullet.rect.top >= screenRect.bottom:
            eBullets.remove(bullet)
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    if setting.interception:
        pg.sprite.groupcollide(bullets, eBullets, bullets, eBullets)


def checkBulletAlienCol(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets):
    """Detect collisions between alien and bullets"""
    collisions = pg.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        sounds.enemy_explosion_sound.play()
        for c in collisions:
            setting.explosions.add(c.rect.x, c.rect.y)

            # Increase the ultimate gauge, upto 100
        stats.ultimateGauge += setting.ultimateGaugeIncrement
        if stats.ultimateGauge > 100:
            stats.ultimateGauge = 100
        for aliens in collisions.values():
            stats.score += setting.alienPoints * len(aliens)
        checkHighScore(stats, sb)
    sb.prepScore()
    # Check if there are no more aliens
    if len(aliens) == 0:
        # Destroy exsiting bullets and create new fleet
        bullets.empty()
        eBullets.empty()
        setting.increaseSpeed()  # Speed up game
        stats.level += 1
        sb.prepLevel()
        time.sleep(1)
        createFleet(setting, screen, ship1, aliens)
        createFleet(setting, screen, ship2, aliens)

        global bgloop
        if stats.level % 5 == 1:
            bgloop += 1
        if bgloop == 3:
            bgloop -= 3
        setting.bgimg(bgloop)


def checkEBulletShipCol(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets):
    """Check for collisions using collision mask between ship and enemy bullets"""
    for ebullet in eBullets.sprites():
        if pg.sprite.collide_mask(ship1, ebullet) or pg.sprite.collide_mask(ship2, ebullet):
            shipHit(setting, stats, sb, screen, ship1, ship2, aliens, bullets, eBullets)
            sb.prepShips()
            eBullets.empty()


def checkHighScore(stats, sb):
    """Check to see if high score has been broken"""
    if stats.score > stats.highScore:
        stats.highScore = stats.score
        sb.prepHighScore()


def checkHighScore(stats, sb):
    """Check to see if high score has been broken"""
    if stats.score > stats.highScore:
        stats.highScore = stats.score
        sb.prepHighScore()


def updateUltimateGauge(setting, screen, stats, sb):
    """Draw a bar that indicates the ultimate gauge"""
    x = sb.levelRect.left - 110
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
    #	elif pattern == 2:
    #		make other pattern
    stats.ultimateGauge = 0


def updateChargeGauge(ship):
    gauge = 0
    if ship.shoot == True:
        gauge = 100 * ((pg.time.get_ticks() - ship.chargeGaugeStartTime) / ship.fullChargeTime)
        if (100 < gauge):
            gauge = 100
    ship.chargeGauge = gauge


def drawChargeGauge(setting, screen, ship1, ship2):
    x1 = 290
    y1 = 50
    x2 = 290
    y2 = 50

    color = (50, 50, 50)
    if (ship1.chargeGauge == 100):
        color = (255, 0, 0)
    elif (50 <= ship1.chargeGauge):
        color = (255, 120, 0)

    pg.draw.rect(screen, (255, 255, 255), (x1, y1, 100, 10), 0)
    pg.draw.rect(screen, color, (x1, y1, ship1.chargeGauge, 10), 0)

    color = (50, 50, 50)
    if (ship2.chargeGauge == 100):
        color = (255, 0, 0)
    elif (50 <= ship2.chargeGauge):
        color = (255, 120, 0)

    pg.draw.rect(screen, (255, 255, 255), (x2, y2, 100, 10), 0)
    pg.draw.rect(screen, color, (x2, y2, ship2.chargeGauge, 10), 0)


def updateScreen(setting, screen, stats, sb, ship1, ship2, aliens, bullets, eBullets, playBtn, menuBtn, quitBtn, sel):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    # Fill the screen with background color
    # Readjust the quit menu btn position
    global x, clock, FPS
    #	playBtn.rect.y = 200
    #	playBtn.msgImageRect.y = 200

    quitBtn.rect.y = 300
    quitBtn.msgImageRect.y = 300

    menuBtn.rect.y = 250
    menuBtn.msgImageRect.y = 250
    # screen.fill(setting.bgColor)
    setting.bgimg(stats.level)
    rel_x = x % setting.bg.get_rect().height
    screen.blit(setting.bg, (0, rel_x - setting.bg.get_rect().height))
    if rel_x < setting.screenHeight:
        screen.blit(setting.bg, (0, rel_x))
    x += 15

    # draw all the bullets
    for bullet in bullets.sprites():
        bullet.drawBullet()

        # draw all the enemy bullets
    for ebull in eBullets.sprites():
        ebull.drawBullet()

    ship1.blitme()
    ship2.blitme()
    aliens.draw(screen)

    # Update Ultimate Gauge
    # updateUltimateGauge(setting, screen, stats, sb)

    updateChargeGauge(ship1)
    updateChargeGauge(ship2)
    drawChargeGauge(setting, screen, ship1, ship2)

    # Draw the scoreboard
    sb.showScore()

    # Draw the play button if the game is inActive
    if not stats.gameActive:
        playBtn.drawBtn()
        menuBtn.drawBtn()
        quitBtn.drawBtn()
        sel.blitme()
    setting.explosions.draw(screen)
    # Make the most recently drawn screen visable.
    pg.display.flip()
    pg.display.update()

    clock.tick(FPS)
