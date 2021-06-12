import pygame
from pygame.locals import *

def loadImage(imageName, colorkey = None, convert = True):
        fullName = imageName + ".png"
        try:
            image = pygame.image.load(fullName)
        except pygame.error as e:
            print("We got an error loading %s!: %s" % (fullName, e))
            raise SystemExit
        
        if convert == True:
            image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

# Button    
def Button(x, y, w, h, text, offColour,onColour, hovColour, txtColour, screen, font, action = None):
    buttonState = "Off"
    mouse = pygame.mouse.get_pos() # Position of the mouse
    click = pygame.mouse.get_pressed() # If the mouse is pressed

    if (x + w > mouse[0] > x) and (y + h > mouse[1] > y):
        if (click[0] == 1):
            if (action is not None and buttonState != "On"):
                action()
            buttonState = "On"
        elif (click[0] != 1):
            buttonState = "Hov"
    else:
        buttonState = "Off"
    
    rectColour = None
    if buttonState == "Off":
        rectColour = offColour
    elif buttonState == "On":
        rectColour = onColour
    elif buttonState == "Hov":
        rectColour = hovColour

    pygame.draw.rect(screen, rectColour, (x, y, w, h))

    textSurf = font.render(str(text), True, txtColour) # Create Text
    textRect = textSurf.get_rect() # Get the rect for the text
    textRect.center = ((x + (w / 2)), (y + (h / 2))) # Put text in place
    screen.blit(textSurf, textRect) # Draw text on screen