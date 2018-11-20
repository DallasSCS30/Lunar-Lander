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
        self.image = pygame.transform.scale(playerImage, (64,64))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/4)
        self.position = vector(WIDTH/2, HEIGHT/4)
        self.velocity = vector(0,0)
        self.thrusting = False
        self.onGround = False
        self.hitGround = False
        self.damaged = False
        self.impactVelocity = 0
        self.rotation = 0
        self.acceleration = vector(0,GRAVITY)
        self.thrust = 0
        
    def magnitudeVelocity(self):
        self.velocityMag = sqrt(self.velocity.x**2 + self.velocity.y**2)
        return self.velocityMag
    


        
    def update(self):          
        
        if self.hitGround:
#            print("On Ground")
            self.impactVelocity = self.magnitudeVelocity()
            self.velocity = vector(0,0)
#            print(self.impactVelocity)
            if self.impactVelocity > 25:
#                print("Crash")
                self.damaged = True 
            elif self.impactVelocity > 0:
#                print("Landed. Takeoff again.")
                pass
            self.hitGround = False
        else:
            self.impactVelocity = 0
        
    
        if self.thrusting:
            self.thrust = THRUST
            self.image = pygame.transform.scale(thrustImage,(64,96))
            self.image.set_colorkey(WHITE)
#            print("Set thrust")
        else:
            self.thrust = 0
            self.image = pygame.transform.scale(playerImage, (64,64))
            self.image.set_colorkey(WHITE)
#            print("Cut engine")
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -0.1
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = 0.1
        
        self.acceleration.y = GRAVITY-self.thrust
                
#        print(self.acceleration)
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.midbottom = self.position
        
        
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH,20))
        self.image.fill(GRAY_75)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-10)
    

def drawText(text, size, color, x, y):
    font = pygame.font.Font(fontName, size)
    textSurface = font.render(text, True, color)
    textRectangle = textSurface.get_rect()
    textRectangle.midtop = (x, y)
    screen.blit(textSurface, textRectangle)  

def showStartScreen():
    screen.fill(BLUE)
    drawText(str("Space bar toggles thrust. Left and right steer."), 20, WHITE, WIDTH / 2, HEIGHT / 2 - 50)
    drawText(str("Press any key to begin. Be ready to use thrust."), 20, WHITE, WIDTH / 2, HEIGHT / 2 + 50)
    pygame.display.flip()
    waitForKey()

def showGameOverScreen():
    screen.fill(BLUE)
    drawText(str("You Crashed"), 48, WHITE, WIDTH/2, HEIGHT/2)
    drawText(str("Press any key to end"), 20, WHITE, WIDTH/2, HEIGHT/2 + 50)
    pygame.display.flip()
    waitForKey()
    return False
    
def waitForKey():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYUP:
                waiting = False

    


## Initialize PyGame and make the empty window.

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Lunar Lander")
clock = pygame.time.Clock()

directory = path.dirname("__file__")
imageDirectory = path.join(directory, "image")
playerImage = pygame.image.load(path.join(imageDirectory, "lander.png")).convert()
backgroundImage = pygame.image.load(path.join(imageDirectory, "background.png")).convert()
backgroundRect = backgroundImage.get_rect()
thrustImage = pygame.image.load(path.join(imageDirectory, "thrusting.png")).convert()

allSprites = pygame.sprite.Group()


player = Player()
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
allSprites.add(player)

ground = Ground()
allSprites.add(ground)

groundGroup = pygame.sprite.Group()
groundGroup.add(ground)

fontName = pygame.font.match_font(FONT_NAME)

showStartScreen()

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
#    print(player.position.y)
    if player.damaged:
        running = False
        

    
    ## Check for ground contact
    hits = pygame.sprite.spritecollide(player, groundGroup, False)
    if hits:
        player.hitGround = True
        player.onGround = True
        player.position.y = hits[0].rect.top + 1
    


    allSprites.update()
    
    ## Render (draw)
    screen.fill(BLACK)
    screen.blit(backgroundImage,backgroundRect)
    allSprites.draw(screen)

    
    ## Flip the display, so the user can see it.
    pygame.display.flip()
    

if player.damaged:
    showGameOverScreen()

pygame.quit()