import objectbase
import peabullet
import time

class PeaShooter(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(PeaShooter,self).__init__(id, pos)
        self.hasBullet = False
        self.hasShoot = False

    def hasSummon(self):
        return self.hasBullet

    def preSummon(self):
        self.hasShoot = True
        self.pathIndex = 0

    def doSummon(self):
        self.hasBullet = False
        return peabullet.PeaBullet(0, (self.pos[0]+20, self.pos[1]+30))

    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getImageIndexCD():
            return
        self.preIndexTime = time.time()

        idx = self.pathIndex + 1
        if idx == 8 and self.hasShoot:
            self.hasBullet = True
        if idx >= self.pathIndexCount:
            idx = 9
        self.updateIndex (idx)
