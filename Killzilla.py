import pygame
import math
import random
from pygame import mixer
#Intializing pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((1800,1000))
#background
background = pygame.image.load('background.jpg')
#music
mixer.music.load('background.wav')
mixer.music.play(-1)

#title and Icon
pygame.display.set_caption("KILLZILLA")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)

#palyer
playerImg = pygame.image.load('player.png')
playerX = 750
playerY = 780
playerX_change = 0
playerY_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
noOfEnemy = 6

for i in range(noOfEnemy):
       enemyImg.append(pygame.image.load('enemy.png'))
       enemyX.append(random.randint(0,1800))
       enemyY.append(random.randint(50,300))
       enemyX_change.append(3)
       enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 780
bulletX_change = 0
bulletY_change = 20
bullet_state = 'ready'

#score
score = 0
font = pygame.font.Font('Lovely Script.otf',32)
textX = 10
textY = 10

def showScore(x,y):
              scor_e = font.render("Score : "+str(score),True,(0,255,0))
              screen.blit(scor_e,(x,y))

#gameOver
overfont = pygame.font.Font('Lovely Script.otf',64)
def gameOverText():
              over = font.render("Game Over", True,(0,255,0))
              x = 750
              y = 780-80
              screen.blit(over,(x,y))

def fireBullet(x,y):
       global bullet_state
       bullet_state = 'fire'
       screen.blit(bulletImg, (x+43,y+20))

def player(x,y):
       screen.blit(playerImg, (x,y))
       
def enemy(x,y,i):
       screen.blit(enemyImg[i], (x,y))

#distance
def isCollision(enemyX,enemyY,bulletX,bulletY):
       distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
       if distance < 27:
              return True
       return False

#game loop
running = True
while running:
       screen.fill((255,255,0))
       #background
       #screen.blit(background, (0,0))
       for event in pygame.event.get():
              if event.type == pygame.QUIT:
                     running = False
              # if any key pressed
              if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LEFT:
                            playerX_change = -5
                     if event.key == pygame.K_RIGHT:
                            playerX_change = 5
                     if event.key == pygame.K_UP:
                            playerY_change = -5
                     if event.key == pygame.K_DOWN:
                            playerY_change = 5
                     if event.key == pygame.K_SPACE:
                            if bullet_state is 'ready':
                                   bulletX = playerX
                                   fireBullet(bulletX,bulletY)
                                   bulletSound = mixer.Sound('laser.wav')
                                   bulletSound.play()
              if event.type == pygame.KEYUP:
                     if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                            #PRINT('Keystroke released')
                            playerX_change = 0
                            playerY_change = 0
       
       #player
       playerX += playerX_change
       if playerX<=0:
              playerX = 0
       elif playerX >= 1700:
              playerX = 1700
       playerY += playerY_change
       player(playerX,playerY)
       
       #enemy
       for i in range(noOfEnemy):
              
              #gameOver
              if enemyY[i] > 700:
                     for j in range(noOfEnemy):
                            enemyY[j] = 3000
                     gameOverText()
                     break
              
              enemyX[i] += enemyX_change[i]
              if enemyX[i]<=0:
                     enemyX_change[i] = 3
                     enemyY[i] += enemyY_change[i]
              elif enemyX[i] >= 1700:
                     enemyX_change[i] = -3
                     enemyY[i] += enemyY_change[i]
              
              enemy(enemyX[i],enemyY[i],i)
              
              collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
              if collision:
                     bulletY = 780
                     bullet_state = 'ready'
                     score+=1
                     #print(score)
                     enemyX[i] = random.randint(0,1800)#750
                     enemyY[i] = random.randint(50,300)
                     collisionSound = mixer.Sound('laser.wav')
                     collisionSound.play()
       
       #bullet movement
       if bulletY <= 0:
              bulletY = 780
              bullet_state = 'ready'
              
       if bullet_state is 'fire':
              fireBullet(bulletX,bulletY)
              bulletY -= bulletY_change
       
       
       showScore(textX,textY)    
       pygame.display.update()
