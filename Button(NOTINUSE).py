import pygame
from pygame.locals import *
class Button:
    def __init__(self, surface, x, y, w, h, action = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.action = action
        self.screen = surface
        self.surf = pygame.Surface((w,h))
        self.rect = self.surf.get_rect()
        self.buttonState = "Off"
        self.rectColour = None

    def checkCollision(self):
        mouse = pygame.mouse.get_pos() # Position of the mouse
        click = pygame.mouse.get_pressed() # If the mouse is pressed
        if (self.x + self.w > mouse[0] > self.x) and (self.y + self.h > mouse[1] > self.y):
            if (click[0] == 1):
                if (self.action is not None and self.buttonState != "On"):
                    self.action()
                self.buttonState = "On"
            elif (click[0] != 1):
                self.buttonState = "Hov"
            else:
                self.buttonState = "Off"
    
    def correctColour(self, offCol, onCol, hovCol):
        if self.buttonState == "Off":
            self.rectColour = offCol
        elif self.buttonState == "On":
            self.rectColour = onCol
        elif self.buttonState == "Hov":
            self.rectColour = hovCol

    def drawMe(self, font, textCol, text):
        textSurf = font.render(str(text), True, textCol) # Create Text
        textRect = textSurf.get_rect() # Get the rect for the text
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2))) # Put text in place
        self.surf.blit(textRect, (0,0))
