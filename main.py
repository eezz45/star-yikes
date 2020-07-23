import pygame
import math
import random
from pygame import mixer

#Initalize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('C:/Users/Yanro/Documents/Python/SpaceInvader/bg.png')

#Background Sound
mixer.music.load('C:/Users/Yanro/Documents/Python/SpaceInvader/igiling.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Yikers")
icon = pygame.image.load('C:/Users/Yanro/Documents/Python/SpaceInvader/alphabet.png')
pygame.display.set_icon(icon)

#Player
playerImg =pygame.image.load('C:/Users/Yanro/Documents/Python/SpaceInvader/user.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 20

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('C:/Users/Yanro/Documents/Python/SpaceInvader/enemy.png'))
    enemyX.append(random.randint(20, 736))
    enemyY.append(random.randint (20, 150))
    enemyX_change.append(1)
    enemyY_change.append(30)

#Bullet

#Ready - You Can't see the bullet on the screen
#Fire - The bullet is currently moving
bulletImg =pygame.image.load('C:/Users/Yanro/Documents/Python/SpaceInvader/bullets.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#gameover text
over_font = pygame.font.Font('freesansbold.ttf', 80)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
#functions of players and enemies

def game_over_text(x,y):
    over_text = font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (350, 250))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Game loop 
running = True
while running:

    #RGB - Red, Green, Blue
    screen.fill((128, 128, 128))
    #Background Image
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            # if event.key == pygame.K_UP:
            #     playerY_change = -1
            # if event.key == pygame.K_DOWN:
            #     playerY_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('C:/Users/Yanro/Documents/Python/SpaceInvader/skadoosh.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
    #Boundaries
    playerX += playerX_change
    playerY += playerY_change
    
    if playerX <=20:
        playerX = 20
    elif playerX >=736:
        playerX = 736
    if playerY <=30:
        playerY = 30
    elif playerY >= 536:
        playerY = 536
    
    #Enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies): 
                enemyY[j] = 2000
            game_over_text(350, 250)
            break

        enemyX[i] += enemyX_change[i]
        #enemyY += enemyY_change
        if enemyX[i] <=20:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        ## if enemyY <=30:
        ##     enemyY_change = 0.1
        ## elif enemyY >= 150:
        ##     enemyY_change = -0.1
    
        collision = isCollision (enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_Sound = mixer.Sound('C:/Users/Yanro/Documents/Python/SpaceInvader/shame.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(20, 736)
            enemyY[i] = random.randint (20, 150)
    
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <=0 :
        bulletY =480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX , bulletY)
        bulletY -= bulletY_change

#colision
    
    
    player(playerX,playerY)
    show_score(textX, textY)
    
    pygame.display.update()      
