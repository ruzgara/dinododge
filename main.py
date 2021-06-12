import pygame, sys, random, time
from pygame.display import update
from pygame.locals import *
from utils import *

from Player import Player
from Enemy import Enemy

def main():
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
    YELLOW = (230, 158, 20)

    DIFFICULTY_COLOR = GREEN

    # Dimensions
    screenWidth = 1000
    screenHeight = 600

    # Balancing Variables
    global gravity
    global moveSpeed

    gravity = 5
    moveSpeed = 5
    increaseInt = 1000 # Increase Interval (increase every x miliseconds)
    increaseBy = 0.6
    enemyIncInt = 3000

    # Score
    global score
    global difficulty

    score = 0
    difficulty = 0
    hiScore = 0

    # Fonts
    font = pygame.font.SysFont("Consolas", 40)
    fontMid = pygame.font.SysFont("Consolas", 30)
    fontSmall = pygame.font.SysFont("Consolas", 20)
    fontTiny = pygame.font.SysFont("Consolas", 8)

    gameOverText = "Game Over (⌐■_■)"

    # Display Setup    
    oddball = loadImage("images/oddball",colorkey=PINK, convert=False)
    pygame.display.set_caption("Game go Brr")
    pygame.display.set_icon(oddball)
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    
    background = loadImage("images/background")
    background.set_alpha(100)
    
    screen.blit(background, (0,0))
    GAMEOVER_COLOUR = (70, 70, 77, 30)
    #-----SETUP END-----

    def addToScore(amount):
        global score
        score += amount


    def gameOverScreen(buttonAction):
        screen.fill(GAMEOVER_COLOUR)

        scoreText = "Score: " + str(score)
        diffText = "Difficulty " + str(difficulty)
        hiScoreText = "Highscore: " + str(hiScore)
        

        # Create fonts
        gameOverScoreFont = fontMid.render(scoreText, True, TURQ)
        gameOverDiffFont = fontMid.render(diffText, True, DIFFICULTY_COLOR)
        gameOverHiScoreFont = fontMid.render(hiScoreText, True, PINK)
        gameOverFont = font.render(gameOverText, True, BLACK)

        # Button Stuff
        buttonx = (screenWidth / 3) - 75
        buttony = (screenHeight / 2) + 150
        Button(buttonx, buttony, 150, 80, "Try Again", BLUE, GREY, TURQ, BLACK, screen, fontSmall, action=buttonAction)
        Button((screenWidth - buttonx - 150), buttony, 150, 80, "Quit", BLUE, GREY, TURQ, BLACK, screen, fontSmall, action=exit)


        # Draw the stuff on
        screen.blit(gameOverFont, ((screenWidth - gameOverFont.get_size()[0])/2, ((screenHeight / 2) - 100)))
        screen.blit(gameOverScoreFont, ((screenWidth - gameOverScoreFont.get_size()[0])/2, (screenHeight / 2) - 50))
        screen.blit(gameOverDiffFont, ((screenWidth - gameOverScoreFont.get_size()[0])/2, (screenHeight / 2)))
        screen.blit(gameOverHiScoreFont, ((screenWidth - gameOverScoreFont.get_size()[0])/2, (screenHeight / 2) + 50))

    # Create sprite groups
    enemies = pygame.sprite.Group()
    players = pygame.sprite.GroupSingle()
    allSprites = pygame.sprite.Group()
    
    def initializeSprites():
        # Add the initial sprites to the groups
            # Create the initial sprites
        P1 = Player(screenWidth, screenHeight, moveSpeed)
        E1 = Enemy(screenWidth, screenHeight, gravity, addToScore)
        enemies.add(E1)
        players.add(P1)
        allSprites.add(P1)
        allSprites.add(E1)

    # Speed game up as time goes on
    SpeedInc = pygame.USEREVENT + 1 # New user event
    EnemyInc = pygame.USEREVENT + 2 # New user event
    pygame.time.set_timer(SpeedInc, increaseInt) #  increase every interval
    pygame.time.set_timer(EnemyInc, enemyIncInt) # increase slower than speed

    # Update Sprite Timer
    #UpdateImageTimer = pygame.USEREVENT + 3
    #pygame.time.set_timer(UpdateImageTimer, int((10000 / FPS)))
    
    initializeSprites()

    # Game Loop
    global gameOn
    gameOn = True
    #updateFrame = False
    while True:
        if (gameOn):
            screen.blit(background, (0,0)) # reset screen

            # Show the score
            scores = fontSmall.render("Score: " + str(score), True, TURQ)
            screen.blit(scores, (10,10))

            # Show the difficulty level
            if difficulty < 15:
                DIFFICULTY_COLOR = GREEN
            if difficulty >= 15:
                DIFFICULTY_COLOR = YELLOW
            if difficulty >= 30:
                DIFFICULTY_COLOR = RED
            difficultyDisplay = fontSmall.render("Difficulty: " + str(difficulty), True, DIFFICULTY_COLOR)
            screen.blit(difficultyDisplay, (10,50))
            
            # For every entity, draw on screen and move
            for entity in allSprites:
                screen.blit(entity.image, entity.rect)
                entity.move()
            for entity in players:
                entity.moveSpeed = moveSpeed
            for entity in enemies:
                entity.gravity = gravity
                #if(updateFrame):
                #    updateFrame = False
                #    entity.updateImage()

            
            # Check for collisions between the player and the enemy
            if pygame.sprite.spritecollideany(players.sprite, enemies):
                gameOn = False # Set game on to be false
        
        else:
            pygame.time.set_timer(SpeedInc, 0) #  increase every interval
            pygame.time.set_timer(EnemyInc, 0) # increase slower than speed
            if score > hiScore:
                hiScore = score

            def restart():
                global score
                global difficulty
                global gameOn
                global gravity
                global moveSpeed

                # Kill all the sprites
                for entity in allSprites:
                    entity.kill()

                score = 0
                difficulty = 0
                pygame.time.set_timer(SpeedInc, increaseInt) #  increase every interval
                pygame.time.set_timer(EnemyInc, enemyIncInt) # increase slower than speed

                gravity = 5
                moveSpeed = 5

                initializeSprites()
                gameOn = True

            pressedKeys = pygame.key.get_pressed() # find if any key is pressed
            if pressedKeys[K_RETURN]: # if the key is enter
                restart() # Restart game

            # Game Over Screen
            gameOverScreen(restart) # Display the game over screen

        watermark = fontTiny.render("Made by DrTipmack", True, RED)
        screen.blit(watermark, ((screenWidth - watermark.get_size()[0]), screenHeight - watermark.get_size()[1]))

        # Go through events
        for event in pygame.event.get():
            # if time to increase speed, increase gravity
            if event.type == SpeedInc:
                gravity += increaseBy # Increase gravity
                moveSpeed += (increaseBy * 0.5) # Increase movespeed
                difficulty += 1 # Increase difficulty

            elif event.type == EnemyInc:
                newEnemy = Enemy(screenWidth, screenHeight, gravity, addToScore) # Create new enemy
                
                # Add enemy to groups
                enemies.add(newEnemy) 
                allSprites.add(newEnemy)

                difficulty += 10 # Increase difficulty
            
            #elif event.type == UpdateImageTimer:
            #    updateFrame = True
            
            # if exited, kill program
            elif event.type == pygame.QUIT:
                sys.exit()

        # make sure game runs at FPS
        FramesPerSecond.tick(FPS)
        pygame.display.update()
if __name__ == "__main__":
    main()