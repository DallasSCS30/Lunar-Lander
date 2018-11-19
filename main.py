##-------------------------------------------------------------------
## Lunar Lander 
## Dallas Spendelow
## November 19, 2018
## A lunar lander game. 
##-------------------------------------------------------------------

import pygame
import random
from settings import *
from os import path
vector = pygame.math.Vector2
from math import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImage, (50,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.position = vector(WIDTH/2, HEIGHT/2)
        self.velocity = vector(0,0)
        self.thrusting = False
        self.onGround = False
        self.impactVelocity = 0
        self.rotation = 0
        self.acceleration = vector(0,GRAVITY)
        self.thrust = vector(0,0)
        self.acceleration = self.acceleration + self.thrust
        self.thrustX = 0
        self.thrustY = 0

    def rotate(self,speed):
        self.rotation = (self.rotation + speed) % 360
        print(self.rotation)
        newImage = pygame.transform.rotate(self.image, self.rotation)
        oldCenter = self.rect.center
        self.image = newImage
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
     
    def rotateThrust(self):
        self.thrustX = float(self.thrustX*cos(radians(self.rotation)) + self.thrustY*sin(radians(self.rotation)))
        self.thrustY = float(-self.thrustX*sin(radians(self.rotation)) + self.thrustY*cos(radians(self.rotation)))
        self.thrust = vector(self.thrustX,self.thrustY)
        
    def update(self):          
        
        if self.onGround:
            if self.impactVelocity > 50:
                print("Crash")
            elif self.impactVelocity > 20:
                print("Minor injuries. Subtracted 100 points to repair.")
            elif self.impactVelocity > 0:
                print("Landed. Takeoff again.")
        
        
        print(self.thrust)
        self.acceleration = vector(0 + self.thrust[0],GRAVITY + self.thrust[1])    
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.midbottom = self.position
        
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = groundImage
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-10)
        

    

## Initialize PyGame and make the empty window.

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Lunar Lander")
clock = pygame.time.Clock()

directory = path.dirname(__file__)
imageDirectory = path.join(directory, "image")
playerImage = pygame.image.load(path.join(imageDirectory, "lander.png")).convert()
groundImage = pygame.image.load(path.join(imageDirectory, "ground.png")).convert()

allSprites = pygame.sprite.Group()


player = Player()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
allSprites.add(player)

ground = Ground()
allSprites.add(ground)

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)



## Main game loop
running = True
while running:
    ## Keep game running at the desired speed
    clock.tick(FPS)
    
    ## Process input (events)
    for event in pygame.event.get():
        ## Check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.thrusting = not player.thrusting
                if player.thrusting:
                    player.thrust = (0,-THRUST)
                    print(player.thrust)
            if event.key == pygame.K_LEFT:
                player.rotate(ROTATION_SPEED)
                player.thrust = player.rotateThrust()
                print(player.thrust)
            if event.key == pygame.K_RIGHT:
                player.rotate(-ROTATION_SPEED)
                player.thrust = player.rotateThrust()
                print(player.thrust)
            
    ## Update
    hits = pygame.sprite.spritecollide(player, groundGroup, False)
    if hits:
        player.onGround = True
        player.impactVelocity = player.velocity.y
        player.position.y = hits[0].rect.top + 1
        player.velocity.y = 0

        
     

    allSprites.update()
    
    ## Render (draw)
    screen.fill(BLACK)
    allSprites.draw(screen)
    
    ## Flip the display, so the user can see it.
    pygame.display.flip()
    
pygame.quit()