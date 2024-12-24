import os
import random

from utils import *


class Enemy(pygame.sprite.Sprite):
        def __init__(self, screenWidth, screenHeight, gravity, scoreUpdate):
            super().__init__()
            self.screenWidth = screenWidth
            self.screenHeight = screenHeight
            self.gravity = gravity
            self.scoreUpdate = scoreUpdate
            self.imgDirPath = "assets/images/Meteors"
            self.imgList = ["assets/images/Meteors/meteor0", "assets/images/Meteors/meteor1", "assets/images/Meteors/meteor2"]
            self.imgs = []
            # for root, dirs, files in os.walk(self.imgDirPath):
            #     for file in files:
            #         self.imgs.append(loadImage(os.path.join(root,file), colorkey=(255,255,255),addExt=False))
            for image in self.imgList:
                self.imgs.append(loadImage(image, colorkey=(255,255,255)))
            self.image = self.imgs[0]
            self.surf = pygame.Surface((self.image.get_size()[0]- 5, self.image.get_size()[1] - 5   )) # define the surface
            self.currentImg = 0
            
            # place enemy at random x value
            self.rect = self.surf.get_rect(center = (random.randint(40, screenWidth - 40), 0))
        
        def move (self):
            self.rect.move_ip(0, self.gravity) # move downwards by gravity
            if self.rect.top > self.screenHeight: # if it has hit the bottom
                self.rect.top = 0 # send back up
                self.scoreUpdate(1)
                self.rect.center = (random.randint(30, self.screenWidth - 30), 0) #at a random x value
                
        def updateImage(self):
            if self.currentImg + 1 == len(self.imgs):
                self.currentImg = 0
            else:
                self.currentImg += 1
            self.image = self.imgs[self.currentImg]

