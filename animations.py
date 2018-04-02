import pygame as pg


class AnimatedSprite:

    def __init__(self, sprite, item_width, item_height, item_count):
        self.sprite = sprite
        self.item_width = item_width
        self.item_height = item_height
        self.item_count = item_count
        self.frames = []

        # extract subsurfaces
        rect = self.sprite.get_rect()
        num_cols = rect.right // item_width
        num_rows = rect.bottom // item_height
        for idx in range(item_count):
            clip_left = (idx % num_cols) * item_width
            clip_top  = (idx // num_rows) * item_height
            clip_rect = pg.Rect(clip_left, clip_top, item_width, item_height)
            self.frames.append(self.sprite.subsurface(clip_rect))

    def getFrame(self, idx):
        return self.frames[idx]

class Animation:

    __slots__ = ('x', 'y', 'frame')

    def __init__(self, x, y, initial_frame=0):
        self.x = x
        self.y = y
        self.frame = initial_frame
        
class Explosions:

    def __init__(self):
        self.sprite = AnimatedSprite(
            pg.image.load('gfx/explosion-sheet.png').convert_alpha(),
            100, 100, 34)
        self.instances = dict()
        self.explosion_id = 0

    def add(self, x, y):
        ani = Animation(x - self.sprite.item_width // 2,
                        y - self.sprite.item_height // 2)
        self.explosion_id += 1
        self.instances[self.explosion_id] = ani

    def draw(self, screen):
        for eid in tuple(self.instances.keys()):
            ani = self.instances[eid]
            rect = pg.Rect(ani.x, ani.y,
                           self.sprite.item_width,
                           self.sprite.item_height)
            screen.blit(self.sprite.getFrame(ani.frame), rect)
            if ani.frame == self.sprite.item_count - 1:
                del self.instances[eid]
            else:
                ani.frame += 1
