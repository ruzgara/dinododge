from utils import *


class Player(pygame.sprite.Sprite):
        def __init__(self, screenWidth, screenHeight, moveSpeed):
            super().__init__()
            self.screenWidth = screenWidth
            self.screenHeight = screenHeight
            self.moveSpeed = moveSpeed
            self.image = loadImage("assets/images/dino", colorkey=(255, 0, 255)) #load the image
            self.orientation = "L"
            self.surf = pygame.Surface(self.image.get_size()) # define the surface
            # place the rectangle at the bottom 10% of the page in the middle            
            self.rect = self.surf.get_rect(midbottom = ((screenWidth / 2), (screenHeight - (screenHeight * 0.1) + 25)))
        
        def move(self):
            pressedKeys = pygame.key.get_pressed() # find if any key is pressed
            if self.rect.left > 0: # if not on edge
                if pressedKeys[K_LEFT] or pressedKeys[K_a]: # if the key is left arrow or a
                    self.rect.move_ip(-self.moveSpeed, 0) # move left by movespeed
                    if self.orientation != "L":
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.orientation = "L"
            if self.rect.right < self.screenWidth: # if not on edge
                if pressedKeys[K_RIGHT] or pressedKeys[K_d]: # if the key is left arrow or d
                    self.rect.move_ip(self.moveSpeed, 0) # move right by movespeed
                    if self.orientation != "R":
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.orientation = "R"
