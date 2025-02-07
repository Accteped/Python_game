import pygame
import sys
from pygame.locals import *
from game import*
from const import *

pygame.init()

DS = pygame.display.set_mode(GAME_SIZE)
game = Game(DS)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.mouseClickHandle(event.button)
    game.update()
    
    DS.fill((255,255,255))
    game.draw()
    pygame.display.update()