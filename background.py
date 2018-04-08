import pygame as pg


class BackgroundManager():
    def __init__(self, screen):
        self.backgrounds = {}
        self.screen = screen
        self.screenRect = screen.get_rect()
        self.active = ''
        self.fillColor = None

    def addBackground(self, name, imagePath, moveSpeedX, moveSpeedY):
        if not name:
            return
        image = pg.image.load(imagePath)
        if name not in self.backgrounds:
            self.backgrounds[name] = []
        bg = Background(self.screen, image, moveSpeedX, moveSpeedY)
        self.backgrounds[name].append(bg)

    def removeBackground(self, name):
        if name in self.backgrounds:
            del self.backgrounds[name]
            self.active = ''

    def getBackground(self, name):
        if name in self.backgrounds:
            return self.backgrounds[name]

    def getSelectedBackground(self):
        if self.active:
            return self.backgrounds[self.active]

    def setFillColor(self, fillColor):
        self.fillColor = fillColor

    def selectBackground(self, name):
        if name in self.backgrounds:
            self.active = name

    def update(self):
        if self.active:
            for bg in self.backgrounds[self.active]:
                bg.update()

    def draw(self):
        if self.active:
            if self.fillColor:
                self.screen.fill(self.fillColor)
            for bg in self.backgrounds[self.active]:
                bg.draw()


class Background():
    def __init__(self, screen, image, moveSpeedX, moveSpeedY):
        self.screen = screen
        self.screenRect = screen.get_rect()
        self.image = image
        self.imageRect = image.get_rect()
        self.x = 0
        self.y = 0
        self.moveSpeedX = moveSpeedX
        self.moveSpeedY = moveSpeedY

    def update(self):
        self.x = (self.x + self.moveSpeedX) % self.imageRect.width
        self.y = (self.y + self.moveSpeedY) % self.imageRect.height

    def draw(self):
        drawX = (-self.imageRect.width + self.x) if (0 < self.x) else self.x
        drawY = (-self.imageRect.height + self.y) if (0 < self.y) else self.y

        while (drawX < self.screenRect.width):
            while (drawY < self.screenRect.height):
                self.screen.blit(self.image, (drawX, drawY))
                drawY += self.imageRect.height
            drawX += self.imageRect.width