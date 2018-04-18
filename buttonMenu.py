import pygame as pg
import pygame.font
from pygame.sprite import *

import utilityFunctions

getInvertedRGB = utilityFunctions.getInvertedRGB


class ButtonMenu():
    def __init__(self, screen):
        self.buttons = {}
        self.menuButtons = []
        self.selected = 0
        self.screen = screen
        self.screenRect = screen.get_rect()
        self.sel = Selector(screen)
        self.margin = 20
        self.btnWidth = 120
        self.btnHeight = 30
        self.x = self.screenRect.centerx - (self.btnWidth / 2)
        self.y = 0

    def addButton(self, name, msg):
        self.buttons[name] = Button(self.screen, msg, self.btnWidth, self.btnHeight)

    def removeButton(self, name):
        if name in self.buttons:
            del self.buttons[name]
        if name in self.menuButtons:
            del self.menuButtons[name]
            self.selected = 0

    def getButton(self, name):
        if name in self.buttons:
            return self.buttons[name]
        else:
            return None

    def getButtons(self):
        return self.buttons

    def getMenuButtons(self):
        return self.menuButtons

    def getSelectedButton(self):
        if self.menuButtons:
            name = self.menuButtons[self.selected]
            return (name, self.buttons[name])
        else:
            return ('', None)

    def getSelectedIdx(self):
        return self.selected

    def setMenuButtons(self, names):
        if (self.menuButtons == names):
            return
        self.menuButtons = []
        self.selected = 0
        for name in names:
            if name in self.buttons:
                self.menuButtons.append(name)

        rectHeight = (self.btnHeight + self.margin) * len(self.menuButtons) - self.margin
        self.y = self.screenRect.centery - (rectHeight / 2)
        self.updateButtonsPos()

    def setButtonSizeAll(self, width=None, height=None):
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        self.btnWidth = width
        self.btnHeight = height
        for name in self.buttons:
            self.buttons[name].setSize(width, height)
        self.updateButtonsPos()

    def setButtonPos(self, name, x, y):
        if name in self.buttons:
            self.buttons[name].setPos(x, y)

    def setPos(self, x=None, y=0):
        if x is None:
            x = self.screenRect.centerx - (self.btnWidth / 2)

        self.x = x
        self.y = y
        self.updateButtonsPos()

    def setMargin(self, margin):
        self.margin = margin
        self.updateButtonsPos()

    def select(self, idx):
        if (0 <= idx < len(self.menuButtons)):
            self.selected = idx

    def selectByName(self, name):
        if name in self.menuButtons:
            self.selected = self.menuButtons.index(name)

    def up(self):
        if (0 < self.selected):
            self.selected -= 1
        else:
            self.selected = len(self.menuButtons) - 1

    def down(self):
        if (self.selected + 1 < len(self.menuButtons)):
            self.selected += 1
        else:
            self.selected = 0

    def updateButtonsPos(self):
        btnY = self.y
        offsetY = self.btnHeight + self.margin
        for name in self.menuButtons:
            self.setButtonPos(name, self.x, btnY)
            btnY += offsetY

    def drawButton(self, name):
        if name in self.buttons:
            self.buttons[name].drawBtn()

    def drawMenuButtons(self):
        for name in self.menuButtons:
            self.drawButton(name)

    def drawSelector(self):
        name, btn = self.getSelectedButton()
        self.sel.setPosByButton(btn)
        self.sel.draw()

    def drawMenu(self):
        self.drawMenuButtons()
        self.drawSelector()

    def mouseCheck(self, mouseX, mouseY):
        for name in self.menuButtons:
            btn = self.buttons[name]
            if btn.rect.collidepoint(mouseX, mouseY):
                return (name, btn)
        return ('', None)

    def invertColorAll(self):
        for name in self.buttons:
            self.buttons[name].invertColor()


class Button():
    def __init__(self, screen, msg, width, height):
        self.screen = screen
        self.msg = msg
        self.rect = pg.Rect(0, 0, width, height)
        self.buttonColor = (255, 255, 255)
        self.textColor = (0, 0, 0)
        self.font = pygame.font.Font('Fonts/Square.ttf', 28)

        self.setText(msg)

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.msgImageRect.center = self.rect.center

    def invertColor(self):
        self.buttonColor = getInvertedRGB(self.buttonColor)
        self.textColor = getInvertedRGB(self.textColor)
        self.setText(self.msg)

    def setText(self, msg):
        self.msgImage = self.font.render(msg, True, self.textColor, self.buttonColor)
        self.msgImageRect = self.msgImage.get_rect()
        self.msgImageRect.center = self.rect.center

    def setSize(self, width, height):
        self.rect.width = width
        self.rect.height = height
        self.msgImageRect.center = self.rect.center

    def updateBtn(self, selected):
        pass

    def drawBtn(self):
        self.screen.fill(self.buttonColor, self.rect)
        self.screen.blit(self.msgImage, self.msgImageRect)


class Selector():
    def __init__(self, screen):
        super(Selector, self).__init__()
        self.screen = screen
        self.image = pg.image.load('gfx/sel.png')
        self.image = pg.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()

    def setPosByButton(self, btn):
        self.rect.x = btn.rect.x + btn.rect.width + 10
        self.rect.centery = btn.rect.centery

    def draw(self):
        self.screen.blit(self.image, self.rect)


class CurrentState():
    def __init__(self, screen, current):
        self.screen = screen
        self.image = pg.image.load('gfx/ebullet.bmp')
        self.image = pg.transform.scale(self.image, (10, 10))
        self.current = current

    def draw(self):
        self.screen.blit(self.image, self.current)
