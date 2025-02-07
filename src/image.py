import pygame
from pygame.locals import *

class Image(pygame.sprite.Sprite):
    def __init__(self, pathFmt, pathIndex, pos, size, pathIndexCount):
        self.pathFmt = pathFmt
        self.pathIndex = pathIndex
        self.pos = list(pos)
        self.size = size
        self.pathIndexCount = pathIndexCount
        self.updateImage()

    def updateImage(self):
        path = self.pathFmt
        if self.pathIndexCount != 0:
            path = path % self.pathIndex
        self.image = pygame.image.load(path)
        if self.size:
            self.image = pygame.transform.scale(self.image, self.size)
    
    def updateSize(self,size):
        self.size = size

    def updateIndex(self, pathIndex):
        self.pathIndex = pathIndex
        self.updateImage()

    def getRect(self):
        rect = self.image.get_rect()
        rect.x,rect.y = self.pos
        return rect

    def doLeft(self):
        self.pos[0] -= 0.5

    def draw(self,ds):
        ds.blit(self.image, self.getRect())