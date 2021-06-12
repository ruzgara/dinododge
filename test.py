import pygame, sys, random, time
from pygame.locals import *

def game():
    #-----SETUP-----

    # Initialise
    pygame.init()

    # Time keeping
    FPS = 60
    FramesPerSecond = pygame.time.Clock()

    # Colours
    RED = (255, 0, 0)
    GREEN = (0, 255 ,0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    TURQ = (34, 190, 211)
    PINK = (255,0,255)
    GREY = (81, 81, 81)

    BACKGROUND_COLOUR = WHITE
    GAMEOVERCOLOUR = RED

    # Usefull later
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

    # Dimensions
    screenWidth = 1000
    screenHeight = 600

    # Balancing Variables
    gravity = 5
    moveSpeed = 5
    increaseInt = 2000 # Increase Interval (increase every x miliseconds)
    increaseBy = 1

    # Score
    global score
    score = 0
    difficulty = 0

    # Fonts
    font = pygame.font.SysFont("Consolas", 40)
    fontMid = pygame.font.SysFont("Consolas", 30)
    fontSmall = pygame.font.SysFont("Consolas", 20)

    gameOverText = "Game Over Noob"

    # Image Setup
    oddball = loadImage("image1",colorkey=PINK, convert=False)
    # background = 

    # Display Setup
    pygame.display.set_caption("Game go Brr")
    pygame.display.set_icon(oddball)
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(BACKGROUND_COLOUR)

    #-----SETUP END-----
    

    # Button
    global buttonState
    buttonState = "Off"
    def Button(x, y, w, h, text, offColour,onColour, hovColour, action = None):
        global buttonState
        mouse = pygame.mouse.get_pos() # Position of the mouse
        click = pygame.mouse.get_pressed() # If the mouse is pressed

        textSurf = fontSmall.render(str(text), True, RED) # Create Text
        textRect = textSurf.get_rect() # Get the rect for the text
        textRect.center = ((x + (w / 2)), (y + (h / 2))) # Put text in place

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

        textSurf = fontSmall.render(str(text), True, RED) # Create Text
        textRect = textSurf.get_rect() # Get the rect for the text
        textRect.center = ((x + (w / 2)), (y + (h / 2))) # Put text in place
        screen.blit(textSurf, textRect) # Draw text on screen

    # Enemy class
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = loadImage("enemy", colorkey=PINK) #load the image
            self.surf = pygame.Surface((56,56)) # define the surface
            # place enemy at random x value
            self.rect = self.surf.get_rect(center = (random.randint(40, screenWidth - 40), 0))
        
        def move (self):
            global score
            self.rect.move_ip(0, gravity) # move downwards by gravity
            if (self.rect.top > screenHeight): # if it has hit the bottom            
                self.rect.top = 0 # send back up
                score += 1
                self.rect.center = (random.randint(30, screenWidth - 30), 0) #at a random x value


    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = loadImage("smiley", PINK) #load the image
            self.surf = pygame.Surface((56,56)) # define the surface
            # place the rectangle at the bottom 10% of the page in the middle            
            self.rect = self.surf.get_rect(midbottom = ((screenWidth / 2), (screenHeight - (screenHeight * 0.1))))
        
        def move(self):
            pressedKeys = pygame.key.get_pressed() # find if any key is pressed
            if (self.rect.left > 0): # if not on edge
                if pressedKeys[K_LEFT] or pressedKeys[K_a]: # if the key is left arrow or a
                    self.rect.move_ip(-moveSpeed, 0) # move left by movespeed
            if (self.rect.right < screenWidth): # if not on edge
                if pressedKeys[K_RIGHT] or pressedKeys[K_d]: # if the key is left arrow or d
                    self.rect.move_ip(moveSpeed, 0) # move right by movespeed

    # Create the initial sprites
    P1 = Player()
    E1 = Enemy()

    # Create sprite groups
    enemies = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()

    # Add the initial sprites to the groups
    enemies.add(E1)
    allSprites.add(P1)
    allSprites.add(E1)

    # Speed game up as time goes on
    SpeedInc = pygame.USEREVENT + 1 # New user event
    EnemyInc = pygame.USEREVENT + 2 # New user event
    pygame.time.set_timer(SpeedInc, increaseInt) #  increase every interval
    pygame.time.set_timer(EnemyInc, increaseInt * 5) # increase slower than speed

    # Game Loop
    gameOver = False
    while gameOver == False:
        screen.fill(BACKGROUND_COLOUR) # reset screen

        # Show the score
        scores = fontSmall.render(str(score), True, BLACK)
        screen.blit(scores, (10,10))

        # Show the difficulty level
        difficultyDisplay = fontSmall.render(str(difficulty), True, BLACK)
        screen.blit(difficultyDisplay, (50,10))
        
        # For every entity, draw on screen and move
        for entity in allSprites:
            screen.blit(entity.image, entity.rect)
            entity.move()
        
        # Check for collisions between the player and the enemy
        if pygame.sprite.spritecollideany(P1, enemies):
            # Kill all the sprites
            for entity in allSprites:
                entity.kill()
            gameOver = True # Set game over to true
        
        # Go through events
        for event in pygame.event.get():
            # if time to increase speed, increase gravity
            if event.type == SpeedInc:
                gravity += increaseBy # Increase gravity
                moveSpeed += (increaseBy * 0.5) # Increase movespeed
                difficulty += 1 # Increase difficulty

            elif event.type == EnemyInc:
                newEnemy = Enemy() # Create new enemy
                print(enemies.sprites())
                
                # Add enemy to groups
                enemies.add(newEnemy) 
                allSprites.add(newEnemy)

                difficulty += 10 # Increase difficulty
            
            # if exited, kill program
            elif event.type == pygame.QUIT:
                sys.exit()

        # make sure game runs at FPS
        FramesPerSecond.tick(FPS)
        pygame.display.update()
    
    # Game Over Screen
    def gameOverScreen(buttonAction):
        screen.fill(GAMEOVERCOLOUR) # Replace screen with game over colour
        # Create fonts
        gameOverScoreFont = fontMid.render(str(score), True, GREY)
        gameOverDiffFont = fontMid.render(str(difficulty), True, GREEN)
        gameOverFont = font.render(gameOverText, True, BLACK)

        # Button Stuff

        buttonx = (screenWidth / 2) - 75
        buttony = (screenHeight / 2) + 150
        Button(buttonx, buttony, 150, 80, "Try Again", BLUE, GREY, TURQ, action=buttonAction)

        # Draw the stuff on
        screen.blit(gameOverFont, ((screenWidth - (font.size(gameOverText)[0]))/2, (screenHeight / 2)))
        screen.blit(gameOverScoreFont, ((screenWidth - (font.size(str(score))[0]))/2, (screenHeight / 2) + 50))
        screen.blit(gameOverDiffFont, ((screenWidth - (font.size(str(score))[0]))/2, (screenHeight / 2) + 100))

    # Stop Timers
    pygame.time.set_timer(SpeedInc, 0)
    pygame.time.set_timer(EnemyInc, 0)

    waiting = True
    while waiting:
        def restart():
            print("Works lmao")
        gameOverScreen(restart) # Display the game over screen

        # check for events
        for event in pygame.event.get():
            # if exited, exit loop
            if event.type == pygame.QUIT:
                sys.exit()
        # make sure game runs at FPS
        FramesPerSecond.tick(FPS)
        pygame.display.update()

game()