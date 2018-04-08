import pygame.font


class Button():
    buttonColor = (255, 255, 255)
    buttonColor1 = (0, 0, 0)
    emp1 = (0, 0, 0)
    textColor = (0, 0, 0)
    textColor1 = (255, 255, 255)
    emp2 = (0, 0, 0)
    """Button Class"""

    def __init__(self, setting, screen, msg, yCord):
        """initialize button attributes"""
        self.screen = screen
        self.screenRect = screen.get_rect()

        # Set the dimensions and properties of the button"""
        self.width, self.height = 100, 30
        self.buttonColor
        self.textColor
        self.font = pygame.font.Font('Fonts/Square.ttf', 28)

        # Buid the button rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screenRect.centerx
        self.rect.y = yCord

        # Set the default state color switch of the button being selected to False
        self.switched = False

        # The button message needs to prepped only once.
        self.prepMsg(msg)

    def reverseCol():
        Button.emp1 = Button.buttonColor
        Button.buttonColor = Button.buttonColor1
        Button.buttonColor1 = Button.emp1
        Button.emp2 = Button.textColor
        Button.textColor = Button.textColor1
        Button.textColor1 = Button.emp2

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
