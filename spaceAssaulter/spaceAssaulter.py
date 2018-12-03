import pygame as pg
import sys
import time
import numpy as np
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
BSPEED = 10
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
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10,20))
        self.speed = BSPEED
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
    def update(self):
        self.rect.x = self.rect.x
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill() 
       
        
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
        elif PRIGHT == True and self.rect.x < WINDOW_WIDTH -25:
            self.rect.x += self.speed
        else :
            pass
        
    def shoot(self):
        newBullet =Bullet(self.rect.x,self.rect.y)
        newBullet.update()
        return newBullet
        
            
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
        self.time = time.time()
    
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
            elif self.rect.x>WINDOW_WIDTH-45:
                self.direction = random.choice([1,4,5])
            elif self.rect.y>WINDOW_HEIGHT-100:
                self.direction = random.choice([1,2,5,6])
            elif self.rect.x<10:
                self.direction = random.choice([2,3,6])
            else: 
                pass

def getMaxTime(Array):
    timeArray=[x.time for x in Array]
    time1 = max(timeArray)
    timeArray.remove(time1)
    time2 = max(timeArray)
    return time1,time2

def EnemyBreeding(enemy1,enemy2,maxLiver1,maxLiver2,gameWindow):
    newEnemy=[]
    if pg.sprite.collide_rect(enemy1,enemy2):
        if enemy1.time==maxLiver1 or enemy2.time==maxLiver1:
            for i in range(2):
                newEnemy.append(Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,i))
        elif enemy1.time == maxLiver2 or enemy2.time == maxLiver2:
            for i in range(2):
                newEnemy.append(Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,i))
    return(newEnemy)            


def playGame(gameWindow,surface_rect,clock):
    rocket = Rocket(gameWindow.get_rect().bottom,gameWindow.get_rect().centerx,gameWindow.get_rect().centery)
    
    probability =np.linspace(0,1,4)
    EnemyArray =[]
    for i in probability:
        EnemyArray.append(Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,i))
    #e1 = Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,0.010)
    #e2 = Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,0.200)
    #e3 = Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,0.005)
    #sprites = pg.sprite.RenderPlain(rocket,tuple(EnemyArray))#e1,e2,e3)
    counter = 0
    bullets=[]
    Score= 0
    score_font = pg.font.SysFont("Helvetica",100)
    while True:
        sprites = pg.sprite.RenderPlain(rocket,tuple(EnemyArray),tuple(bullets))
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
                if event.key == K_SPACE:
                    bullet=rocket.shoot()
                    #bullet.update()
                    bullets.append(bullet)
            
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    PLEFT = False
                    PRIGHT = False
                    NOMOVE = True
                if event.key == K_RIGHT:
                    PLEFT = False
                    PRIGHT = False
                    NOMOVE = True
                #if event.key == K_UP:
                    
        for fire in bullets:
            fire.update()
            
        gameWindow.fill(BLACK)
        sprites.draw(gameWindow)
        for enemy in EnemyArray:
            enemy.move()
            enemy.changeDirection(counter)
        
        if(counter%8==0):
            for enemy in EnemyArray:
                for secenemy in EnemyArray:
                    if (enemy != secenemy and len(EnemyArray)<=100):
                        maxtime1,maxtime2= getMaxTime(EnemyArray)
                        newEnemy=EnemyBreeding(enemy,secenemy,maxtime1,maxtime2,gameWindow)
            EnemyArray+=newEnemy
        
        for enemy in EnemyArray:
            for fire in bullets:
                if pg.sprite.collide_rect(enemy,fire):
                    enemy.kill()
                    fire.kill()
                    Score = Score+10
                    EnemyArray.remove(enemy)
                    bullets.remove(fire)
                    break
        scoreBoard = score_font.render(str(Score)+True,WHITE,BLACK)
        scoreBoard_rect = scoreBoard.get_rect()
        scoreBoard_rect.centerx = surface_rect.centerx
        scoreBoard_rect.y = 10
        #mainWindow.blit(scoreBoard,scoreBoard_rect)
        #print(EnemyArray)
# =============================================================================
#         e1.move()
#         e1.changeDirection(counter)
#         e2.move()
#         e2.changeDirection(counter)
#         e3.move()
#         e3.changeDirection(counter)
# =============================================================================
        rocket.move()
        pg.display.update()
        counter +=1
        if counter ==1000000:
            counter =0
        if(len(EnemyArray)>100):
            sys.exit()

                
def getClock():
    return pg.time.Clock()

def createGameWindow(width,height):
    flag = 0
    depth =32
    return pg.display.set_mode((width,height),flag,depth)
    
def main():
    gameWindow = createGameWindow(WINDOW_WIDTH,WINDOW_HEIGHT)
    surface_rect = gameWindow.get_rect()
    pg.display.set_caption('SPACE ASSAULTER GAME')
    clock = getClock()
    playGame(gameWindow,surface_rect,clock)
    
if __name__=='__main__':
    pg.init()
    main()    