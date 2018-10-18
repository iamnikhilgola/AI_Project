import pygame as pg
import sys
import time
from pygame.locals import *
from random import randint

#Global Variables********
#Game window size parameter
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 650

#Paddle Variables------- 
#Paddle Speed limit 
PONG_PADDLE_SPEED = 7

#Paddle1
MOVE_UP1 = False
MOVE_DOWN1 = False
NO_MOVE1 = True

#Paddle2    
MOVE_UP2 = False
MOVE_DOWN2 = False
NO_MOVE2 = True

#Ball Variables-------
FWD_LEFT = 0
BWD_LEFT = 1
FWD_RIGHT =2
BWD_RIGHT =3

#Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
GREEN = (0,255,0)
BLUE = (0, 0, 255)

# BALL CLASS
class Ball(pg.sprite.Sprite):
    def __init__(self,centerx,centery):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([10,10])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.direction = randint(0,3)
        self.speed = 4
    def move(self):
        if self.direction ==FWD_LEFT:
            self.rect.x -=self.speed
            self.rect.y -=self.speed
        elif self.direction ==FWD_RIGHT:
            self.rect.x +=self.speed
            self.rect.y -=self.speed 
        elif self.direction ==BWD_LEFT:
            self.rect.x -=self.speed
            self.rect.y +=self.speed
        elif self.direction ==BWD_RIGHT:
            self.rect.x +=self.speed
            self.rect.y +=self.speed
            
    def changeDirection(self,bottom):
       if self.rect.y <0 and self.direction==FWD_LEFT:
           self.direction = BWD_LEFT
       if self.rect.y<0 and self.direction == FWD_RIGHT:
           self.direction = BWD_RIGHT
       if self.rect.y > bottom and self.direction == BWD_LEFT:
           self.direction = FWD_LEFT
       if self.rect.y > bottom and self.direction == BWD_RIGHT:
           self.direction = FWD_RIGHT
                
# PADDLE CLASS 
class Paddle(pg.sprite.Sprite):
    def __init__(self,playerID,xleft,xright,centery):
        #Paddle Spirit
        pg.sprite.Sprite.__init__(self)
        self.xleft = xleft
        self.xright = xright
        self.centery = centery
        self.playerID = playerID
        
        self.image = pg.Surface([10,100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 7
        # Paddle Location
        if self.playerID ==0:
            self.rect.centerx = self.xleft
            self.rect.centerx +=50
        elif self.playerID ==1:
            self.rect.centerx = self.xright
            self.rect.centerx -=50
        self.rect.centery = self.centery
    def move(self):
        global MOVE_UP1
        global MOVE_UP2
        global MOVE_DOWN1
        global MOVE_DOWN2
        global NO_MOVE1
        global NO_MOVE2
        if self.playerID == 0:
            if (MOVE_UP1==True) and (self.rect.y>5):
                
                self.rect.y -=self.speed
            elif (MOVE_DOWN1==True) and (self.rect.bottom <WINDOW_HEIGHT-5):
                self.rect.y +=self.speed
            elif (NO_MOVE1==True):
                pass
            
        if self.playerID == 1:
            if (MOVE_UP2==True) and (self.rect.y>5):
                print("unable to move")
                self.rect.y -=self.speed
            elif (MOVE_DOWN2==True) and (self.rect.bottom <WINDOW_HEIGHT-5):
                self.rect.y +=self.speed
            elif (NO_MOVE2==True):
                pass
def paddle_ballHit(paddle1,paddle2,ball):
    if pg.sprite.collide_rect(ball,paddle2):
        if ball.direction == FWD_RIGHT:
            ball.direction = FWD_LEFT
        elif ball.direction ==BWD_RIGHT:
            ball.direction = BWD_LEFT
        ball.speed *= 1.01
    if pg.sprite.collide_rect(ball,paddle1):
        if ball.direction == FWD_LEFT:
            ball.direction = FWD_RIGHT
        elif ball.direction ==BWD_LEFT:
            ball.direction = BWD_RIGHT
        ball.speed *= 1.01
    
                
#Game Play
def playGame(mainWindow,surface_rect,clock):
    paddle1 = Paddle(0,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
    paddle2 = Paddle(1,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
    ball = Ball(surface_rect.centerx,surface_rect.centery)
    sprites = pg.sprite.RenderPlain(paddle1,paddle2,ball)
    p1_Score = 0
    p2_score = 0
    count =0
    while True:
        clock.tick(60)
        if ball.rect.x >WINDOW_WIDTH:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(0,1)
            ball.speed = 4
            p1_Score+=1
        elif ball.rect.x<0:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(2,3)
            ball.speed = 4
            p2_score+=1
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                global MOVE_UP1
                global MOVE_UP2
                global MOVE_DOWN1
                global MOVE_DOWN2
                global NO_MOVE1
                global NO_MOVE2
                if event.key == ord('w'):
                    MOVE_UP1= True
                    MOVE_DOWN1 = False
                    NO_MOVE1 = False
                elif event.key == ord('s'):
                    MOVE_UP1= False
                    MOVE_DOWN1 = True
                    NO_MOVE1 = False  
                elif event.key == K_UP:
                    MOVE_UP2= True
                    MOVE_DOWN2 = False
                    NO_MOVE2 = False
                elif event.key ==K_DOWN:
                    MOVE_UP2= False
                    MOVE_DOWN2 = True
                    NO_MOVE2 = False
            if event.type == KEYUP:
                
                if event.key==ord('w') or event.key == ord('s'):
                    MOVE_UP1= False
                    MOVE_DOWN1 = False
                    NO_MOVE1 = True
                if event.key ==K_DOWN or event.key==K_UP:
                    MOVE_UP2= False
                    MOVE_DOWN2 = False
                    NO_MOVE2 = True

        mainWindow.fill(BLACK)
        sprites.draw(mainWindow)
        paddle1.move()
        paddle2.move()
        ball.move()
        ball.changeDirection(surface_rect.bottom)
        paddle_ballHit(paddle1,paddle2,ball)
        pg.display.update()
        
# Getting the clock for the Game
def getClock():
    return pg.time.Clock()

#creating the Game window 
def createGameWindow(width,height):
    return pg.display.set_mode((width,height),0,32)


def main():
    mainWindow = createGameWindow(WINDOW_WIDTH,WINDOW_HEIGHT)
    surface_rect = mainWindow.get_rect()
    clock = getClock()
    playGame(mainWindow,surface_rect,clock)
if __name__ =='__main__':
    pg.init()
    main()