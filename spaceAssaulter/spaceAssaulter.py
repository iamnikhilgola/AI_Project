import pygame as pg
import sys
import time
from pygame.locals import *
from random import randint
import random

# Global Values
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 650

#Enemy Movement
UP_LEFT = 1
UP_RIGHT = 2
DOWN_RIGHT = 3
DOWN_LEFT = 4
LEFT = 5
RIGHT = 6

#Player Movement
PLEFT = False
PRIGHT = False
NOMOVE = True

#Bullet speed
BSPEED = 40
SHOOT = False

#Color Vairables 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Agent List
AGENTS = []
class Bullet(pg.sprite.Sprite):
    def __init__(self,centerx,centery,speed):
        pg.sprite.Sprite.__init__(self)
        self.centerx = centerx
        self.centery = centery
        self.image = pg.Surface([2,3])
        self.speed = speed
        self.image.fill(RED)
        self.rect = self.image.get_rect()
    
       
        
class Rocket(pg.sprite.Sprite):
    def __init__(self,bottom,centerx,centery):
        pg.sprite.Sprite.__init__(self)
        self.centerx = centerx
        self.centery = centery
        self.bottom = bottom
        self.image = pg.Surface([20,20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 7
        self.rect.centerx = self.centerx
        self.rect.centery = self.bottom-10
    
    def move(self):
        if (PLEFT == True) and (self.rect.x>5):
            self.rect.x -=self.speed
        elif PRIGHT == True and self.rect.x < WINDOW_WIDTH -20:
            self.rect.x += self.speed
        else :
            pass
    def shoot(self):
        pass
            
class Enemy(pg.sprite.Sprite):
    def __init__(self,centerx,centery,probMoving):
        pg.sprite.Sprite.__init__(self)
        self.centerx = centerx
        self.centery = centery
        self.probMoving = probMoving
        self.direction = randint(1,6)
        self.image = pg.Surface([50,50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.speed = randint(1,5)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
    
    def move(self):
        if self.direction == UP_LEFT:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        
        elif self.direction == UP_RIGHT:
            self.rect.x += self.speed
            self.rect.y -= self.speed
            
        elif self.direction == DOWN_RIGHT:
            self.rect.x += self.speed
            self.rect.y += self.speed
        
        elif self.direction == DOWN_LEFT:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        
        elif self.direction == RIGHT:
            self.rect.x += self.speed
            self.rect.y =self.rect.y
        
        elif self.direction == LEFT:
            self.rect.x -= self.speed
    def changeDirection(self,counter):
        if counter%10 ==0:
            r = randint(0,1000)
            p = 1000*self.probMoving
            if r<=p:
                self.direction= randint(1,6)
        else:
            if self.rect.y<0:
                self.direction = random.choice([3,4,5,6])
            elif self.rect.y>WINDOW_HEIGHT-100:
                self.direction = random.choice([1,2,5,6])
            elif self.rect.x<10:
                self.direction = random.choice([2,3,6])
            elif self.rect.x>WINDOW_WIDTH-10:
                self.direction = random.choice([1,4,5])
            else: 
                pass
def playGame(gameWindow,surface_rect,clock):
    rocket = Rocket(gameWindow.get_rect().bottom,gameWindow.get_rect().centerx,gameWindow.get_rect().centery)
    e1 = Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,0.010)
    e2 = Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,0.200)
    e3 = Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,0.005)
    sprites = pg.sprite.RenderPlain(rocket,e1,e2,e3)
    counter =0
    while True:
        clock.tick(60)
        for event in pg.event.get():
            global PLEFT
            global PRIGHT
            global NOMOVE
            if event.type ==QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key==K_LEFT:
                    PLEFT =True
                    PRIGHT = False
                    NOMOVE = False
                if event.key == K_RIGHT:
                    PLEFT = False
                    PRIGHT = True
                    NOMOVE = False
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    PLEFT = False
                    PRIGHT = False
                    NOMOVE = True
                if event.key == K_RIGHT:
                    PLEFT = False
                    PRIGHT = False
                    NOMOVE = True
                    
        gameWindow.fill(BLACK)
        sprites.draw(gameWindow)
        e1.move()
        e1.changeDirection(counter)
        e2.move()
        e2.changeDirection(counter)
        e3.move()
        e3.changeDirection(counter)
        rocket.move()
        pg.display.update()
        counter +=1
        if counter ==1000000:
            counter =0

                
def getClock():
    return pg.time.Clock()
def createGameWindow(width,height):
    flag = 0
    depth =32
    return pg.display.set_mode((width,height),flag,depth)
    
def main():
    gameWindow = createGameWindow(WINDOW_WIDTH,WINDOW_HEIGHT)
    surface_rect = gameWindow.get_rect()
    clock = getClock()
    playGame(gameWindow,surface_rect,clock)
    
if __name__=='__main__':
    pg.init()
    main()    