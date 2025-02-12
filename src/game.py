import image
import time
import random
from pygame.locals import *
import pygame
import data_object
import sunflower
import zombiebase
import peashooter
import sys
from const import *

class Game(object):
    def __init__(self,ds):
        self.ds = ds
        self.back = image.Image(PATH_BACK, 0 ,(0,0), GAME_SIZE, 0)
        self.lose = image.Image(PATH_LOSE, 0 ,(0,0), GAME_SIZE, 0)
        self.plants = []
        self.hasPlant = []
        self.zombies = []
        self.summons = []
        self.goldFont = pygame.font.Font(None, 60)
        self.gold = 100
        self.zombie = 0
        self.zombieFont = pygame.font.Font(None, 60)
        self.zombieGenertateTime = 0
        self.isGameOver = False
        for i in range(GRID_SIZE[0]):
            col = []
            for j in range(GRID_SIZE[1]):
                col.append(0)
            self.hasPlant.append(col)
    
    def renderFont(self):
        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 23))

        textImage = self.goldFont.render("Gold: " + str(self.gold), True, (255, 255, 255))
        self.ds.blit(textImage, (13, 23))

        textImage = self.goldFont.render("Score: " + str(self.zombie), True, (0, 0, 0))
        self.ds.blit(textImage, (13, 83))

        textImage = self.goldFont.render("Score: " + str(self.zombie), True, (255, 255, 255))
        self.ds.blit(textImage, (13, 80))

    def draw(self):
        self.back.draw(self.ds)
        for plant in self.plants:
            plant.draw(self.ds)
        for summon in self.summons:
            summon.draw(self.ds)
        for zombie in self.zombies:
            zombie.draw(self.ds)
        self.renderFont()
        if self.isGameOver:
            self.lose.draw(self.ds)

    def update(self):
        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            summon.update()
        for zombie in self.zombies:
            zombie.update()
        
        if time.time() - self.zombieGenertateTime > ZOMBIE_BORN_CD:
            self.zombieGenertateTime = time.time()
            self.addZombie(ZOMBIE_BORN_X, random.randint(0, GRID_COUNT[1]-1))

        for smmon in self.summons:
            if summon.getRect().x > GAME_SIZE[0] or summon.getRect().y > GAME_SIZE[1]:
                self.summons.remove(summon)
                break

        for zombie in self.zombies:
            zombie.update()
            if zombie.getRect().x < 0:
                self.isGameOver = True

        self.checkSummonVSZombie()
        self.checkZombieVSPlant()

    def fight(self, a, b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False
        return False

    def checkZombieVSPlant(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie, plant)
                    if plant.hp <= 0:
                        self.plants.remove(plant)
                        return
        
    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                        self.zombie += 1 
                    if summon.hp <= 0:
                        self.summons.remove(summon)
                    return 

    def addZombie(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = zombiebase.ZombieBase(1, pos)
        self.zombies.append(zm)

    def addSunFlower(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sf = sunflower.SunFlower(SUNFLOWER_ID, pos)
        self.plants.append(sf)

    def addPeaShooter(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sf = peashooter.PeaShooter(PEASHOOTER_ID, pos)
        self.plants.append(sf)
    
    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold += summon.getPrice()
                return True
        return False

    def getIndexByPos(self,mousePos):
        x,y = mousePos
        Pos = []
        f = 0
        for i in range(GRID_COUNT[0]):
            if x >= i * GRID_SIZE[0]+LEFT_TOP[0] and x <= (i+1) * GRID_SIZE[0]+LEFT_TOP[0]:
                Pos.append(i) 
                f = 1
        if(f == 0):
           Pos.append(-1)
        f = 0
        for i in range(GRID_COUNT[1]):
            if y >= i * GRID_SIZE[1]+LEFT_TOP[1] and y <= (i+1) * GRID_SIZE[1]+LEFT_TOP[1]:
                Pos.append(i)
                f = 1
        if(f == 0):
           Pos.append(-1)
        return Pos


    def checkAddPlant(self, mousePos, objId):
        x,y = self.getIndexByPos(mousePos)
        if x < 0 or x >= GRID_COUNT[0]:
            return 
        if y < 0 or y >= GRID_COUNT[1]:
            return
        if self.gold < data_object.data[objId]['PRICE']:
            return
        if self.hasPlant[x][y] != 0:
            return
        
        self.hasPlant[x][y] = 1
        self.gold -= data_object.data[objId]['PRICE']
        if objId == SUNFLOWER_ID:
            self.addSunFlower(x,y)
        elif objId == PEASHOOTER_ID:
            self.addPeaShooter(x,y)

    def mouseClickHandle(self, btn):
        mousePos = pygame.mouse.get_pos()
        if self.isGameOver:
            return
        if(self.checkLoot(mousePos)):
            return
        if btn == 1:
            self.checkAddPlant(mousePos, SUNFLOWER_ID)
        elif btn == 3:
            self.checkAddPlant(mousePos, PEASHOOTER_ID)
