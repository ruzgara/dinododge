import pygame
import random
from pygame.locals import *
from utils import *

class Enemy(pygame.sprite.Sprite):
        def __init__(self, screenWidth, screenHeight, gravity, scoreUpdate):
            super().__init__()
            self.screenWidth = screenWidth
            self.screenHeight = screenHeight
            self.gravity = gravity
            self.scoreUpdate = scoreUpdate
            self.base = loadImage("images/meteor_base", colorkey=(255, 0, 255)) #load the image
            self.surf = pygame.Surface((48,76)) # define the surface
            # place enemy at random x value
            self.rect = self.surf.get_rect(center = (random.randint(40, screenWidth - 40), 0))
            #self.fires = [loadImage("images/fire" + str(i), colorkey= (255, 0, 255)) for i in [1,2]]
            self.image = loadImage("images/gimp/meteor", colorkey= (255, 255, 255))
            #self.base.blit(self.fires[1])
            #self.fireNum = 1
        
        def move (self):
            self.rect.move_ip(0, self.gravity) # move downwards by gravity
            if (self.rect.top > self.screenHeight): # if it has hit the bottom            
                self.rect.top = 0 # send back up
                self.scoreUpdate(1)
                self.rect.center = (random.randint(30, self.screenWidth - 30), 0) #at a random x value
                
        """ def updateImage(self):
            if self.fireNum == 1:
                self.base.blit(self.fires[2])
                self.fireNum = 2
            elif self.fireNum == 2:
                self.base.blit(self.fires[2])
                self.fireNum = 1 """
