import random

from utils import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, gravity, screenWidth, screenHeight, maxHeight, updateScore, font):
        super().__init__()
        self.screenHeight = screenHeight
        self.gravity = gravity
        self.maxHeight = maxHeight
        self.value = random.randint(-40, 40)
        self.color = "gold"
        self.img = "assets/images/Coins/green"
        if self.value < 0:
            self.img = "assets/images/Coins/red"
        self.image = loadImage(self.img, (255,255,255))
        self.surf = pygame.Surface(self.image.get_size())  # define the surface
        self.rect = self.surf.get_rect(center=(random.randint(40, screenWidth - 40), 0))
        self.tslm = 5 # time since last move
        self.updateScore = updateScore
        self.animate = False
        self.x = self.rect.x
        self.y = self.rect.y
        #textSurf = font.render(str(self.value), True, BLACK)
        textSurf = font.render("A", False, BLACK)

        textRect = textSurf.get_rect() # Get the rect for the text
        textRect.center = (self.rect.x + (self.image.get_size()[0] / 2),
                           (self.y + (self.image.get_size()[1] / 2))) # Put text in place
        self.image.blit(textSurf, textRect)

    def move(self):
        self.tslm -= 1
        if self.rect.bottom < self.maxHeight:
            self.rect.move_ip(0, self.gravity) # move downwards by gravity
            self.tslm += 1
        elif self.tslm < 1:
            self.rect.move_ip(0, 2)
            self.tslm = 5
        if self.rect.top > self.screenHeight:
            self.kill()

    def pickup(self):
        self.updateScore(self.value)