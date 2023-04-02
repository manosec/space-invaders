import pygame
import random
import math
from pygame import mixer
import os

#Initialize pygame
pygame.init()

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(os.getcwd()+"/images/spaceship.png")
pygame.display.set_icon(icon)

#Creating the screen for the pygame
screen  = pygame.display.set_mode((800, 600))

#Background Image
backgroundImg = pygame.image.load(os.getcwd()+"/images/background.png")

#Background Music
mixer.music.load(os.getcwd()+"/sounds/background.wav")
mixer.music.play(-1) #To play in loop -1 should be there(need to check again) 

#Adding Player as img
playerImg = pygame.image.load(os.getcwd()+"/images/player.png")
playerX_cord = 380
playerY_cord = 500
playerX_change = 0
playerY_change = 0

#Adding Enemy
num_of_enemy = 5

enemyImg = []
enemyX_cord = []
enemyY_cord = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load(os.getcwd()+"/images/alien.png"))
    enemyX_cord.append(random.randint(0, 735))
    enemyY_cord.append(random.randint(0, 100))
    enemyX_change.append(7)
    enemyY_change.append(80)


#Adding Bullet
bulletImg = pygame.image.load(os.getcwd()+"/images/bullet.png")
bulletX_cord = 0
bulletY_cord = 480
bulletY_change = 20
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font(os.getcwd()+"/fonts/Spring_Snowstorm.ttf", 32)
textX = 10
textY = 10

#Game_over 
over_font = pygame.font.Font(os.getcwd()+"/fonts/Spring_Snowstorm.ttf", 64)

#Socials
profile_font = pygame.font.Font(os.getcwd()+"/fonts/Spring_Snowstorm.ttf", 20)

def show_score(x, y):
    score = font.render("Score: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
    
def game_over():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(270, 250))
    
def show_social():
    profile = profile_font.render("Twitter : @manosec", True, (255,255,255))
    screen.blit(profile, (680, 10))
    
def player(x, y):
    screen.blit(playerImg, (x, y))
    
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16 ,y+10))
    
def collision_detect(enemyX_cord, enemyY_cord, bulletX_cord, bulletY_cord):
    distance = math.sqrt((math.pow(enemyX_cord-bulletX_cord,2)) + (math.pow(enemyY_cord-bulletY_cord,2))) 
    if distance < 27:
        return True
    return False
    
running = True
while running:
    #Screen(Game) Background set
    screen.fill((0,0,0))
    screen.blit(backgroundImg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -15
            if event.key == pygame.K_RIGHT:
                playerX_change = 15
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound(os.getcwd()+"/sounds/laser.wav")
                    bullet_sound.play()
                    bulletX_cord = playerX_cord
                    fire_bullet(bulletX_cord, bulletY_cord)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0                
    
    
    #Player Movement & Boundary
    playerX_cord += playerX_change
    
    if playerX_cord <= 0:
        playerX_cord = 0
    if playerX_cord >= 735:
        playerX_cord = 735
        
    #Enemy Movement and boundry
    for i in range(num_of_enemy):
        enemyX_cord[i] += enemyX_change[i]
        if enemyY_cord[i] > 440:
            for j in range(num_of_enemy):
                enemyY_cord[j] = 2000
            game_over()    
                
        if enemyX_cord[i] <= 0:
            enemyX_change[i] = 7
            enemyY_cord[i] += enemyY_change[i]
            
        if enemyX_cord[i] >= 735:
            enemyX_change[i] = -7
            enemyY_cord[i] += enemyY_change[i]
        #Detect Collision(Enemy&bullet)
        collision = collision_detect(enemyX_cord[i],enemyY_cord[i],bulletX_cord,bulletY_cord)
        if collision:
            destroyed_sound = mixer.Sound(os.getcwd()+"/sounds/explosion.wav")
            destroyed_sound.play()
            bullet_state = "ready"
            bulletY_cord = 480
            score_value += 10
            enemyX_cord[i] = random.randint(0, 735)
            enemyY_cord[i] = random.randint(0, 100)
        enemy(enemyX_cord[i], enemyY_cord[i], i)
        
    #Bullet Movement
    if bulletY_cord <= 0:
        bulletY_cord = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX_cord, bulletY_cord)
        bulletY_cord -= bulletY_change
    
    show_social()
    show_score(textX, textY)
    player(playerX_cord, playerY_cord)
    pygame.display.update()