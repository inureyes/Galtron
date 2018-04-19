import pygame.font

import utilityFunctions

buttons = []
getInvertedRGB = utilityFunctions.getInvertedRGB


class Button():
    """Button Class"""

    def __init__(self, setting, screen, msg, yCord):
        """initialize button attributes"""
        self.screen = screen
        self.screenRect = screen.get_rect()

        # Set the dimensions and properties of the button"""
        self.width, self.height = 100, 30
        self.buttonColor = (255, 255, 255)
        self.textColor = (0, 0, 0)
        self.font = pygame.font.Font('Fonts/Square.ttf', 28)

        # Buid the button rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screenRect.centerx
        self.rect.y = yCord

        # Set the default state color switch of the button being selected to False
        self.switched = False

        self.msg = msg
        self.prepMsg(msg)

        buttons.append(self)

    def __del__(self):
        if self in buttons:
            buttons.remove(self)

    def invertColorAll():
        for btn in buttons:
            btn.invertColor()

    def invertColor(self):
        self.buttonColor = getInvertedRGB(self.buttonColor)
        self.textColor = getInvertedRGB(self.textColor)
        self.prepMsg(self.msg)

    def prepMsg(self, msg):
        """Turn msg insto a rendered image and center text on the button"""
        self.msgImage = self.font.render(msg, True, self.textColor, self.buttonColor)
        self.msgImageRect = self.msgImage.get_rect()
        self.msgImageRect.center = self.rect.center

    def updateBtn(self, selected):
        pass

    def drawBtn(self):
        # Draw blank button and then draw message
        self.screen.fill(self.buttonColor, self.rect)
        self.screen.blit(self.msgImage, self.msgImageRect)
