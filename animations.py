import pygame as pg
from pygame.sprite import Sprite, Group
from pygame import Rect, Surface

class Explosions():
	def __init__(self):
		self.ExplosionEffects=Group()

	def draw(self, screen):
		self.ExplosionEffects.update()
		self.ExplosionEffects.draw(screen)

	def add(self, x, y):
		newExplosionEffect = ExplosionEffect(x, y)
		self.ExplosionEffects.add(newExplosionEffect)

class ExplosionEffect(Sprite):
	def __init__(self, x, y):
		super(ExplosionEffect, self).__init__()
		self.cellWidth = 100
		self.cellHeight = 100
		self.spriteSheet = SpriteSheet('gfx/explosion-sheet.png', self.cellWidth, self.cellHeight)
		self.rect = Rect(x - (self.cellWidth / 2), y - (self.cellHeight / 2), self.cellWidth, self.cellHeight)
		self.frame = 0
		self.frameTime = 2
		self.dtime = 0

	def update(self):
		self.image = self.spriteSheet.getImage(self.frame)
		if self.image != None:
			self.dtime += 1
			if self.frameTime <= self.dtime:
				self.frame += 1
				self.dtime = 0
		else:
			self.kill()

class SpriteSheet():
	def __init__(self, spriteSheetPath, cellWidth, cellHeight):
		self.spriteSheet = pg.image.load(spriteSheetPath).convert_alpha()
		self.spriteSheetRect = self.spriteSheet.get_rect()
		self.cellWidth = cellWidth
		self.cellHeight = cellHeight
		self.image = Surface([cellWidth, cellHeight], pg.SRCALPHA, 32)
		self.imageRect = self.image.get_rect()
		self.frameCol = (self.spriteSheetRect.width // self.cellWidth)
		self.frameRow = (self.spriteSheetRect.height // self.cellHeight)
		self.frames = self.frameCol * self.frameRow

	def getImage(self, frame):
		if frame < self.frames:
			cellX = self.cellWidth * (frame % self.frameCol)
			cellY = self.cellHeight * (frame // self.frameRow)
			cellRect = Rect(cellX, cellY, self.cellWidth, self.cellHeight)
			self.image.fill((0,0,0,0))
			self.image.blit(self.spriteSheet, self.imageRect, cellRect)
			return self.image
		else:
			return None
 