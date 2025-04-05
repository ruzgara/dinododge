import random
import asyncio
import pygame

from Coin import Coin
from Enemy import Enemy
from Player import Player
from utils import *

import sys

async def main():
    #-----SETUP-----

    # Initialise
    pygame.init()

    # Time keeping
    FPS = 60
    FramesPerSecond = pygame.time.Clock()

    DIFFICULTY_COLOR = GREEN

    # Dimensions
    screenWidth = 1000
    screenHeight = 600

    # Balancing Variables
    global gravity
    global moveSpeed
    global maxEnemyNum
    global maxSpeed

    debugMode = False

    maxEnemyNum = 7
    maxSpeed = 10

    gravity = 5 # initial gravity
    moveSpeed = 8 # initial move speed
    speedIncreaseInt = 3000 # Increase Interval (increase every x miliseconds)
    speedIncreaseBy = 0.6 # Amount to increase by
    enemyIncreaseInt = 5000

    enemyDifficultyCoef = 10
    speedDifficultyCoef = 1
    maxDifficulty = enemyDifficultyCoef * maxEnemyNum + speedDifficultyCoef * maxSpeed

    # Score
    global score
    global difficulty

    # Fonts

    font = pygame.font.Font(resource_path("assets/fonts/Press-Start.ttf"), 30)
    fontMid = pygame.font.Font(resource_path("assets/fonts/Press-Start.ttf"), 20)
    fontSmall = pygame.font.Font(resource_path("assets/fonts/Press-Start.ttf"), 15)
    fontTiny = pygame.font.Font(resource_path("assets/fonts/Press-Start.ttf"), 5)

    score = 0
    difficulty = 0
    hiScore = 0

    gameOverText = "Game Over :("

    # music
    #pygame.mixer.music.load(resource_path("assets/music/mainMusic.ogg"))

    # Display Setup
    dinoMan = loadImage("assets/images/dino", colorkey=PINK, convert=False)
    pygame.display.set_caption("DinoDodge")
    pygame.display.set_icon(dinoMan)
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    background = loadImage("assets/images/background")
    background.set_alpha(100)

    screen.blit(background, (0,0))
    GAMEOVER_COLOUR = (70, 70, 77, 30)
    #-----SETUP END-----

    def gameOverScreen(buttonAction):
        alpha = pygame.Surface((screenWidth, screenHeight))
        alpha.set_alpha(1)
        alpha.fill(BLACK)
        screen.blit(alpha, (0, 0))

        scoreText = "Score: " + str(score)
        diffText = "Difficulty: " + str(difficulty)
        if difficulty >= maxDifficulty:
            diffText = "Difficulty: MAX"

        hiScoreText = "Highscore: " + str(hiScore)


        # Create fonts
        gameOverScoreFont = fontMid.render(scoreText, True, TURQ)
        gameOverDiffFont = fontMid.render(diffText, True, DIFFICULTY_COLOR)
        gameOverHiScoreFont = fontMid.render(hiScoreText, True, PINK)
        gameOverFont = font.render(gameOverText, True, WHITE)

        # Button Stuff
        buttonx = (screenWidth / 3) - 75
        buttony = (screenHeight / 2) + 150
        #Button(buttonx, buttony, 150, 80, "Try Again", BLUE, GREY, BLACK, screen, fontSmall, action=buttonAction)
        #Button((screenWidth - buttonx - 150), buttony, 150, 80, "Quit", BLUE, GREY, BLACK, screen, fontSmall, action=exit)
        ImgButton(buttonx, buttony, 150, 80, "assets/images/Buttons/normal",
                  "assets/images/Buttons/hov", screen, "Try Again", BLACK, fontSmall, buttonAction)
        ImgButton((screenWidth - buttonx - 150), buttony, 150, 80, "assets/images/Buttons/normal",
                  "assets/images/Buttons/hov", screen, "Quit", BLACK, fontSmall, sys.exit)

        # Draw the stuff on
        screen.blit(gameOverFont, ((screenWidth - gameOverFont.get_size()[0])/2, ((screenHeight / 2) - 100)))
        screen.blit(gameOverScoreFont, ((screenWidth - gameOverScoreFont.get_size()[0])/2, (screenHeight / 2) - 50))
        screen.blit(gameOverDiffFont, ((screenWidth - gameOverScoreFont.get_size()[0])/2, (screenHeight / 2)))
        screen.blit(gameOverHiScoreFont, ((screenWidth - gameOverScoreFont.get_size()[0])/2, (screenHeight / 2) + 50))

    def pauseScreen(buttonAction):
        pauseFont = font.render("Game Paused", True, WHITE)
        screen.blit(pauseFont, ((screenWidth - pauseFont.get_size()[0])/2, ((screenHeight / 2) - 100)))
        alpha = pygame.Surface((screenWidth, screenHeight))
        alpha.set_alpha(25)
        alpha.fill(GAMEOVER_COLOUR)
        screen.blit(alpha, (0,0))
        ImgButton((screenWidth / 2) - 50, (screenHeight / 2) - 50, 100, 100, "assets/images/icons/play-norm",
                  "assets/images/icons/play-hov", screen, action=pauseButtonAct, colorkey=PINK)
    
    # Create sprite groups
    enemies = pygame.sprite.Group()
    players = pygame.sprite.GroupSingle()
    coins = pygame.sprite.Group()
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


    # Update Sprite Timer
    UpdateImageTimer = pygame.USEREVENT + 3
#    pygame.time.set_timer(UpdateImageTimer, int((10000 / FPS)))

    # Game Loop
    global gameState
    gameState = "S" # R: running, P: pause, D:dead/game over, S:splash-screen
    updateFrame = False
    enemyIncFrame = False
    speedIncFrame = False
    firstRunningFrame = True
    firstSplashFrame = True
    animationMoveFrame = False

    titleY = 0
    nameY = 0
    dinoY = 0

    flip = False
    tslf = 0

    pauseCountDown = 0
    global coinCountDown
    coinCountDown = 5

    def addToScore(amount):
        global score
        global coinCountDown
        score += amount
        coinCountDown -= 1

    def coinValueUpdate(amount):
        global score
        score += amount

    def killCoin(coinToKill):
        coins.remove(coinToKill)

    while True:
        pressedKeys = pygame.key.get_pressed()  # find if any key is pressed

        if pauseCountDown > 0:
            pauseCountDown -= 1

        def pauseButtonAct():
                global gameState
                if gameState == "P":
                    gameState = "R"
                elif gameState == "R":
                    gameState = "P"
        if gameState == "R":
            if firstRunningFrame:
                firstRunningFrame = False

            screen.blit(background, (0,0)) # reset screen
            
            if enemyIncFrame:
                newEnemy = Enemy(screenWidth, screenHeight, gravity, addToScore) # Create new enemy
                
                # Add enemy to groups
                enemies.add(newEnemy)
                allSprites.add(newEnemy)

                difficulty += enemyDifficultyCoef # Increase difficulty
                
                enemyIncFrame = False
            
            if speedIncFrame:
                gravity += speedIncreaseBy # Increase gravity
                moveSpeed += (speedIncreaseBy * 0.5) # Increase movespeed
                difficulty += speedDifficultyCoef # Increase difficulty

                speedIncFrame = False

            if coinCountDown == 0:
                coinCountDown = 5
                coin = Coin(gravity, screenWidth, screenHeight, (screenHeight - (screenHeight * 0.1) + 25), coinValueUpdate, fontSmall)
                coins.add(coin)
                allSprites.add(coin)

            # Show the score
            scores = fontSmall.render("Score: " + str(score), True, TURQ)
            screen.blit(scores, (10,10))

            # Show the difficulty level
            if difficulty < maxDifficulty/4:
                DIFFICULTY_COLOR = GREEN
            if difficulty >= maxDifficulty/2:
                DIFFICULTY_COLOR = YELLOW
            if difficulty >= maxDifficulty/1.5:
                DIFFICULTY_COLOR = RED
            diffTxt = "Difficulty: " + str(difficulty)
            if difficulty >= maxDifficulty:
                diffTxt = "Difficulty: MAX"

            difficultyDisplay = fontSmall.render(diffTxt, True, DIFFICULTY_COLOR)
            screen.blit(difficultyDisplay, (10,50))

            #Show pause button
            ImgButton((screenWidth - 50), 0, 40, 40, "assets/images/icons/pause-norm",
                      "assets/images/icons/pause-hov", screen, action=pauseButtonAct, colorkey=PINK)

            if pressedKeys[K_p] and pauseCountDown == 0:  # if the key is "P"
                pauseButtonAct()  # Pause game
                pauseCountDown = 10

            
            # For every entity, draw on screen and move
            for entity in players:
                entity.moveSpeed = moveSpeed
            for entity in enemies:
                entity.gravity = gravity
                if updateFrame:
                    entity.updateImage()
            for entity in allSprites:
                screen.blit(entity.image, entity.rect)
                entity.move()
            
            if updateFrame:
                    updateFrame = False

            
            # Check for collisions between the player and the enemy
            if debugMode == False and pygame.sprite.spritecollideany(players.sprite, enemies):
                gameState = "D" # Set gamestate to be D for dead

            coinCollide = pygame.sprite.spritecollide(players.sprite, coins, True)
            if len(coinCollide) != 0:
                coinCollide[0].pickup()

        elif gameState == "D":
            pygame.time.set_timer(SpeedInc, 0) #  increase every interval
            pygame.time.set_timer(EnemyInc, 0) # increase slower than speed
            coinCountDown = 5
            if score > hiScore:
                hiScore = score

            def restart():
                global score
                global difficulty
                global gameState
                global gravity
                global moveSpeed

                # Kill all the sprites
                for entity in allSprites:
                    entity.kill()

                score = 0
                difficulty = 0
                pygame.time.set_timer(SpeedInc, speedIncreaseInt) #  increase every interval
                pygame.time.set_timer(EnemyInc, enemyIncreaseInt) # increase slower than speed

                gravity = 5
                moveSpeed = 5

                initializeSprites()
                gameState = "R"

            if pressedKeys[K_RETURN]: # if the key is enter
                restart() # Restart game
            elif pressedKeys[K_q]: # if the key is "Q"
                exit() # Exit game

            # Game Over Screen
            gameOverScreen(restart) # Display the game over screen

        elif gameState == "P":
            pauseScreen(pauseButtonAct)
            if pressedKeys[K_p] and pauseCountDown == 0:  # if the key is "P"
                pauseButtonAct()  # Un-Pause game
                pauseCountDown = 10

        elif gameState == "S":
            def startGame():
                global gravity
                global moveSpeed
                global gameState
                global firstRunningFrame
                gameState = "R" # It will run next frame
                pygame.time.set_timer(animationMove, 0) # Stop the animationMove timer
                pygame.time.set_timer(SpeedInc, speedIncreaseInt)  # increase every interval
                pygame.time.set_timer(EnemyInc, enemyIncreaseInt)  # increase slower than speed
                pygame.time.set_timer(UpdateImageTimer, 100)
                initializeSprites()
                gravity = 5
                moveSpeed = 5
                # pygame.mixer.music.play(-1, fade_ms=200)

            animationMove = pygame.USEREVENT + 4 # Define animationMove timer

            #Set fonts
            titleFont = font.render("DinoDodge", True, BLACK)
            nameFont = fontSmall.render("By Rüzgar Altıner", True, BLACK)

            if firstSplashFrame:
                pygame.time.set_timer(animationMove, 1000)
                titleY = (screenHeight / 2) - titleFont.get_size()[1]
                nameY = (screenHeight / 2) + 15
                dinoY = (screenHeight / 2) - titleFont.get_size()[1] - 15
                firstSplashFrame = False

            if animationMoveFrame:
                x = random.randint(1, 5)
                if x == 1 or x == 2:
                    if titleY == (screenHeight / 2) - titleFont.get_size()[1]:
                        titleY = titleY + 5
                    else:
                        titleY = titleY - 5
                elif x == 3 or x == 4:
                    if nameY == (screenHeight / 2) + 15:
                        nameY = nameY + 5
                    else:
                        nameY = nameY - 5

                if dinoY == (screenHeight / 2) - titleFont.get_size()[1] - 15:
                    dinoY = dinoY - 5
                else:
                    dinoY = dinoY + 5

                if flip and tslf > 1:
                    flip = False
                    tslf = 0
                elif not flip and tslf > 1:
                    flip = True
                    tslf = 0
                tslf += 1

            animationMoveFrame = False
            screen.fill(GAMEOVER_COLOUR)

            ImgButton((screenWidth - 250) / 2, (screenHeight / 2) + 100, 250, 80, "assets/images/Buttons/big-normal",
                      "assets/images/Buttons/big-hov", screen, "Start Game", BLACK, fontMid, startGame, PINK)
            if pressedKeys[K_RETURN]: # if the key is enter
                startGame() # Start game

            # Draw the fonts
            screen.blit(titleFont, ((screenWidth - titleFont.get_size()[0]) / 2, titleY))
            screen.blit(nameFont, ((screenWidth - nameFont.get_size()[0]) / 2, nameY))

            # Draw dino

            dino = loadImage("assets/images/dino", PINK)
            newSize = (dino.get_size()[0] * 3, dino.get_size()[1] * 3)
            dino = pygame.transform.scale(dino, newSize)
            if flip:
                dino = pygame.transform.flip(dino, True, False)

            dinoSurf = pygame.Surface(dino.get_size())
            dinoRect = dinoSurf.get_rect(midbottom=(screenWidth / 2, dinoY))
            screen.blit(dino, dinoRect)
        watermark = fontTiny.render("Made by Rüzgar Altıner", True, RED)
        screen.blit(watermark, ((screenWidth - watermark.get_size()[0]), screenHeight - watermark.get_size()[1]))

        # Go through events
        for event in pygame.event.get():
            # if time to increase speed, increase gravity
            if event.type == SpeedInc:
                if gameState == "R":
                    speedIncFrame = True

            elif event.type == EnemyInc:
                if gameState == "R":
                    enemyIncFrame = True
            
            elif event.type == UpdateImageTimer:
                updateFrame = True

            elif event.type == animationMove:
                animationMoveFrame = True
            
            # if exited, kill program
            elif event.type == pygame.QUIT:
                sys.exit()
        
        if len(enemies.sprites()) == maxEnemyNum:
            pygame.time.set_timer(EnemyInc, 0)
        if gravity * speedIncreaseBy >= maxSpeed:
            pygame.time.set_timer(SpeedInc, 0)

        # make sure game runs at FPS
        FramesPerSecond.tick(FPS)
        await asyncio.sleep(0)
        pygame.display.update()
if __name__ == "__main__":
    asyncio.run(main())