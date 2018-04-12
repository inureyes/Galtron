import pygame as pg

from settings import Settings

setting = Settings()
screen = pg.display.set_mode((setting.screenWidth, setting.screenHeight))


# load and change images
def introimages():
    while (pg.time.get_ticks() < 3000):
        introImageSrc = ("gfx/intro1.png",
                         "gfx/intro2.png",
                         "gfx/intro3.png",
                         "gfx/intro4.png",
                         "gfx/intro5.png",
                         "gfx/intro6.png",
                         "gfx/intro7.png")

        for src in introImageSrc:
            image = pg.image.load(src)
            image = pg.transform.scale(
                image, (setting.screenWidth, setting.screenHeight))
            rect = image.get_rect()
            screen.fill(setting.bgColor)
            screen.blit(image, rect)
            pg.display.update()

            waitTime = 400
            if src == introImageSrc[-1]:
                waitTime += 200
            pg.time.wait(waitTime)
            print("load", src, waitTime)
