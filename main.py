##-------------------------------------------------------------------
## Lunar Lander 
## Dallas Spendelow
## November 14, 2018
## A lunar lander game. 
##-------------------------------------------------------------------

import pygame
import random
from settings import *
import os
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,75))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.position = vector(WIDTH/2, HEIGHT/2)
        self.velocity = vector(0,0)
        self.acceleration = vector(0,GRAVITY)
        self.thrusting = False
        self.onGround = False
        self.hitGround = False
        self.impactVelocity = 0

    def whenOnGround(self):
        self.rect.bottom = HEIGHT-20
        if self.impactVelocity > 100:
            print("Crash!")
            showGameOverScreen()
        elif self.impactVelocity > 50:
            print("Minor injuries.")
        else:
            print("Landed.")
        
        
    def update(self):          
        
        if self.thrusting:
##            print("Engine firing.")   
            self.acceleration = vector(0,GRAVITY-THRUST)
        else:
            self.acceleration = vector(0,GRAVITY)


##        self.acceleration = vector(0,GRAVITY)
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.midbottom = self.position
        
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH,20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-10)            

## Initialize PyGame and make the empty window.

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Lunar Lander")
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()

player = Player()
allSprites.add(player)

ground = Ground()
allSprites.add(ground)



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
            
    ## Update
    player.onGround = pygame.sprite.collide_rect(player, ground)
    player.impactVelocity = player.velocity.y
    while player.onGround:
        player.whenOnGround()
        

    allSprites.update()
    
    ## Render (draw)
    screen.fill(BLACK)
    allSprites.draw(screen)
    
    ## Flip the display, so the user can see it.
    pygame.display.flip()
    
pygame.quit()