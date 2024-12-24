import os
import sys

import pygame
from pygame.locals import *

# Colours
RED = (255, 0, 0)
GREEN = (0, 255 ,0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TURQ = (34, 190, 211)
PINK = (255,0,255)
GREY = (81, 81, 81)
YELLOW = (230, 158, 20)

def loadImage(imageName, colorkey = None, convert = True, addExt = True):
    if addExt:
        imageName = imageName + ".png"
    try:
        image = pygame.image.load(resource_path(imageName))
    except pygame.error as e:
        print("We got an error loading %s!: %s" % (imageName, e))
        raise SystemExit

    if convert:
        image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Button    
def Button(x, y, w, h, text, offColour, hovColour, txtColour, screen, font, action = None):
    buttonState = "Off"
    mouse = pygame.mouse.get_pos() # Position of the mouse
    click = pygame.mouse.get_pressed() # If the mouse is pressed

    if (x + w > mouse[0] > x) and (y + h > mouse[1] > y):
        if click[0] == 1:
            if action is not None and buttonState != "On":
                action()
            buttonState = "On"
        elif click[0] != 1:
            buttonState = "Hov"
    else:
        buttonState = "Off"
    
    rectColour = None
    if buttonState == "Off":
        rectColour = offColour
    elif buttonState == "Hov":
        rectColour = hovColour

    pygame.draw.rect(screen, rectColour, (x, y, w, h))

    textSurf = font.render(str(text), True, txtColour) # Create Text
    textRect = textSurf.get_rect() # Get the rect for the text
    textRect.center = ((x + (w / 2)), (y + (h / 2))) # Put text in place
    screen.blit(textSurf, textRect) # Draw text on screen

def ImgButton(x, y, w, h, offImgPath, hovImgPath, screen, text=None, txtColour=None, font=None, action=None, colorkey=None):
    global buttonState
    buttonState = "Off"
    mouse = pygame.mouse.get_pos() # Position of the mouse
    click = pygame.mouse.get_pressed() # If the mouse is pressed

    if (x + w > mouse[0] > x) and (y + h > mouse[1] > y):
        if click[0] == 1:
            buttonState = "On"
        elif click[0] != 1:
            buttonState = "Hov"
    else:
        buttonState = "Off"

    imagePath = ""
    if buttonState == "Off":
        imagePath = offImgPath
    elif buttonState == "Hov":
        imagePath = hovImgPath
    elif buttonState == "On":
        if action is not None:
            action()
            buttonState = "Hov"
        imagePath = hovImgPath
    
    image = loadImage(imagePath, colorkey, True)
    rect = image.get_rect(topleft=(x,y))
    screen.blit(image,rect)

    if text is not None:
        textSurf = font.render(str(text), True, txtColour) # Create Text
        textRect = textSurf.get_rect() # Get the rect for the text
        textRect.center = ((x + (w / 2)), (y + (h / 2))) # Put text in place
        screen.blit(textSurf, textRect) # Draw text on screen