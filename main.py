# Author: Rachita Jain
import math
import pygame
import random
from pygame import mixer  # handles all kind of music related work

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # create screen
# background image from www.freepik.com-> make sure it is of same size as screen
background = pygame.image.load('background.jpg')

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)   # -1 used to play the music in loop. Also, mixer.music is for prolonged music.

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 510
playerX_change = 0  # change in player's x values

# Enemy  (for multiple enemies)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))  # so that enemy respawns in random places
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)  # change in player's x values
    enemyY_change.append(40)  # 40 pixels it moves down after completing one horizontal line of motion

# bullet
# ready state - can't see bullet nn screen
# fire state - bullet is currently moving
bulletImg = pygame.image.load('bullet.png')  # 32 pix
bulletX = 0
bulletY = 510  # has to be at the same level as spaceship
bulletY_change = 10  # slower than enemy
bullet_state = 'ready'

# Title and Icon  -> images/icons- flaticon.com
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 28)   # pygame's free font. for any other free font visit dafont.com and
# download the ttf file to project folder
textX = 10 # coordinate for text
textY = 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)


# to show text in pygame, it has to be rendered first and the blitted
def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))   # centre of the screen


def player(x, y):
    screen.blit(playerImg, (x, y))  # to build the image of player on the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # blit function controls what appears on the screen
    screen.blit(bulletImg, (x + 16, y + 20))  # adjusting in accordance with spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 20:    # an estimate - open for experiment
        return True
    else:
        return False


# game loop -> makes sure that game is running-> only exits when cross pressed
running = True
while running:

    screen.fill((0, 0, 0))  # rgb values for screen
    # background image added
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # loop through all the events
        if event.type == pygame.QUIT:  # if cross button pressed
            running = False

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:  # key down is pressing any key
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:  # space bar for bullet
                if bullet_state is "ready":  # multiple pressing of space bar can lead to change in x coordinate so
                    # add this if statement to avoid that condition
                    bullet_Sound = mixer.Sound("laser.wav")  # .sound is used for only momentary sounds
                    bullet_Sound.play()
                    bulletX = playerX  # saving the initial x coordinate of spaceship so that the bullet does not follow
                    # the changing coordinates of spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # check if the key is released
            if event.key == pygame.K_LEFT or \
                    event.key == pygame.K_RIGHT:
                playerX_change = 0  # so that spaceship stops when key is released

    # checking for boundaries
    playerX += playerX_change
    if playerX < 0:  # to eliminate the chance of going beyond left boundary
        playerX = 0
    elif playerX >= 736:  # 800 - size of spaceship i.e 64
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 460:  # when any enemy crosses 300 pix, game over
            for j in range(num_of_enemies):
                enemyY[j] = 2000   # move all the enemies out of screen and break out of loop
            game_over_text()
            mixer.music.stop()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # to eliminate the chance of going beyond left boundary
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800 - size of enemy i.e 64
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")  # .sound is used for only momentary sounds
            explosion_Sound.play()
            bulletY = 510  # to initialize the bullet again
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)  # respawn the enemy after kill
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # to specify which enemy is blitted

    # Bullet movement
    if bulletY <= 0:
        bulletY = 510
        bullet_state = "ready"
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  # so that bullet moves up in y direction

    player(playerX, playerY)  # inside while loop so that always show on the screen
    show_score(textX, textY)
    pygame.display.update()  # so that screen keeps updating
