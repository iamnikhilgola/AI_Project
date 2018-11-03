
import pygame as pg
import sys
import time
from pygame.locals import *
from random import randint
from random import uniform
from random import shuffle

#Global Variables********
#Game window size parameter
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 650

#Paddle Variables------- 
#Paddle Speed limit 
PONG_PADDLE_SPEED = 1

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

#fonts 
score_font = None

geneSet =[]

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
        self.speed = 15
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
        self.speed = 25
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
                
                self.rect.y -=self.speed
            elif (MOVE_DOWN2==True) and (self.rect.bottom <WINDOW_HEIGHT-5):
                self.rect.y +=self.speed
            elif (NO_MOVE2==True):
                pass
def doMove(playerID,gene,px,py,bx,by):
    p1= gene[0]
    c1 = gene[1]
    c2 = gene[2]
    p2= gene[3]
    c3 = gene[4]
    c4 = gene[5]
    x = px - bx 
    y = py - by
    
    number = uniform(0,1)
    if number < p1: 
        if x < 0 and y < 0:
            getMove(1,c1)
            #print("moving for -x -y","px: ",px," py: ",py," bx: ",bx," by:",by)
        elif x < 0 and y > 0:
            getMove(1,c2)
            #print("moving for -x +y","px: ",px," py: ",py," bx: ",bx," by:",by)
    if number < p2:
        if x > 0 and y < 0:
            getMove(2,c3)
            #print("moving for +x -y","px: ",px," py: ",py," bx: ",bx," by:",by)
        elif x > 0 and y >0:
            getMove(2,c4)
            #print("moving for +x +y","px: ",px," py: ",py," bx: ",bx," by:",by)
            
            
def getMove(playerID,c):
    if c>=0.0 and c<0.3:
        moveDown(playerID)
    elif c >=0.3 and c <0.7:
        noMove(playerID)
    elif c >=0.7 and c <= 1:
        moveUp(playerID)
def moveUp(playerID):
        global MOVE_UP1
        global MOVE_UP2
        global MOVE_DOWN1
        global MOVE_DOWN2
        global NO_MOVE1
        global NO_MOVE2
        
        if playerID ==1:
             MOVE_UP1= True
             MOVE_DOWN1 = False
             NO_MOVE1 = False
        if playerID ==2:
            MOVE_UP2= True
            MOVE_DOWN2 = False
            NO_MOVE2 = False
def moveDown(playerID):
        global MOVE_UP1
        global MOVE_UP2
        global MOVE_DOWN1
        global MOVE_DOWN2
        global NO_MOVE1
        global NO_MOVE2
        
        if playerID ==1:
             MOVE_UP1= False
             MOVE_DOWN1 = True
             NO_MOVE1 = False
        if playerID ==2:
            MOVE_UP2= False
            MOVE_DOWN2 = True
            NO_MOVE2 = False
def noMove(playerID):
        global MOVE_UP1
        global MOVE_UP2
        global MOVE_DOWN1
        global MOVE_DOWN2
        global NO_MOVE1
        global NO_MOVE2
        
        if playerID ==1:
             MOVE_UP1= False
             MOVE_DOWN1 = False
             NO_MOVE1 = True
        if playerID ==2:
            MOVE_UP2= False
            MOVE_DOWN2 = False
            NO_MOVE2 = True
def paddle_ballHit(paddle1,paddle2,ball):
    if pg.sprite.collide_rect(ball,paddle2):
        if ball.direction == FWD_RIGHT:
            ball.direction = FWD_LEFT
        elif ball.direction ==BWD_RIGHT:
            ball.direction = BWD_LEFT
        ball.speed *= 1
    if pg.sprite.collide_rect(ball,paddle1):
        if ball.direction == FWD_LEFT:
            ball.direction = FWD_RIGHT
        elif ball.direction ==BWD_LEFT:
            ball.direction = BWD_RIGHT
        ball.speed *= 1
    return 1

def selection(pop):
    shuffle(pop)
    return pop
    
def mutation(C1,prob):
    x = uniform(0,1)
    
    if x <= prob:
        point = randint(0,len(C1)-1)
        point2 = randint(0,len(C1)-1)
        C1[point] = round(uniform(0,1),3)
        C1[point2] = round(uniform(0,1),3)
    return C1
def crossover(C1,C2,x):
    point = randint(1,len(C1)-1)
    if x ==0:
        f1 = C1[:point]
        f2 = C2[:point]
        b1 = C1[point:]
        b2 = C2[point:]
        CH1 = f1 + b2
        CH2 = f2 + b1
        return CH1,CH2
    else:
        return [],[]
    
def generatePopulation(x):
    pop = [] 
    while len(pop)<x:
        p = round(uniform(0,1),3)
        gene =[p,round(uniform(0,1),3),round(uniform(0,1),3),round(uniform(0,1),3),round(uniform(0,1),3),round(uniform(0,1),3)]
        if gene not in pop and gene not in geneSet:
            pop.append(gene)
            geneSet.append(gene)
    return pop
def fitness(gene,relayTime,rallyTime,c):
    f = rallyTime - (relayTime/c)
    #print(f)
    #print("relay : ",relayTime," RallyTime :",rallyTime," Fitness: ",f," c:",c," div:",relayTime/c)
    return [gene,f]

def getKey(chm):
    return chm[1]

def calculateFitness(mainWindow,surface_rect,clock,gene,generation):
    re,ra,w = playGame(mainWindow,surface_rect,clock,gene,generation)
    return fitness(gene,re,ra,w)
                 
#Game Play
def getMinimumFitness(popF):
    minm = +9999999.9999
    for p in popF:
        t = p[1]
        if t < minm:
            minm = t
    return minm
    
def geneticAlgorithm(mainWindow,surface_rect,clock):
    length = 10
    pop = generatePopulation(length)
    generation = 1
    popF = []
    for p in pop:
        popF.append(calculateFitness(mainWindow,surface_rect,clock,p,generation))
        #print(popF)
    minF =+99999.999
    ccurf = getMinimumFitness(popF)
    for ran in range(100):
    #while minF >= ccurf and minF>2:
        print(ccurf)
        generation+=1
        minF = ccurf
        popF = selection(popF)
        newpop =[]
        for i in range(0,len(popF),2):
            x,y = crossover(popF[i][0],popF[i+1][0],0)
            x = mutation(x,0.5)
            y = mutation(x,0.5)
            if x not in geneSet:
                newpop.append(x)
                geneSet.append(x)
            if y not in geneSet:
                newpop.append(y)
                geneSet.append(y)
        if len(newpop) < length:
            newpop = newpop + generatePopulation(length-len(newpop))
        for p in newpop:
            popF.append(calculateFitness(mainWindow,surface_rect,clock,p,generation))
        popF = sorted(popF,key=getKey)
        popF = popF[:len(pop)]
        ccurf = getMinimumFitness(popF)
        
       
        
        

def playGame(mainWindow,surface_rect,clock,gene,generation):
    paddle1 = Paddle(0,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
    paddle2 = Paddle(1,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
    ball = Ball(surface_rect.centerx,surface_rect.centery)
    sprites = pg.sprite.RenderPlain(paddle1,paddle2,ball)
    p1_Score = 0
    p2_Score = 0
    paddleHit = 0
    score_font = pg.font.SysFont("Helvetica",100)
    timeFont  =pg.font.SysFont("Helvetica",20)
    timeFont2  =pg.font.SysFont("Helvetica",20)
    genFont = pg.font.SysFont("Helvetica",20)
    startTime = time.time()
    rstartTime = time.time()
    rallyTime = 0.00
    relayTime = 0.00
    
    count =0
    while True:
        clock.tick(60)
        
        if ball.rect.x >WINDOW_WIDTH:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(0,1)
            ball.speed = 15
            p1_Score+=1
            rstartTime = time.time()
        elif ball.rect.x<0:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(2,3)
            ball.speed = 15
            p2_Score+=1
            rstartTime = time.time()
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
        doMove(1,gene,paddle1.rect.x,paddle1.rect.y,ball.rect.x,ball.rect.y)
        doMove(2,gene,paddle2.rect.x,paddle2.rect.y,ball.rect.x,ball.rect.y)
        relayTime = time.time()-startTime   
        rallyTime = max(rallyTime,time.time()-rstartTime)
        scoreBoard = score_font.render(str(p1_Score)+"\t\t"+str(p2_Score),True,WHITE,BLACK)
        scoreBoard_rect = scoreBoard.get_rect()
        scoreBoard_rect.centerx = surface_rect.centerx
        scoreBoard_rect.y = 10
        
        timeStr = str(relayTime)
        timeStr2 = str(rallyTime)
        timeStr2 = timeStr2[:8]
        timeStr = timeStr[:8]
        
        relaytimeboard = timeFont.render("Relay Time : "+timeStr,True,WHITE,BLACK)
        relaytimeboard_rect = relaytimeboard.get_rect()
        relaytimeboard_rect.x = 15
        relaytimeboard_rect.y = 10
        
        
        rallytimeboard = timeFont2.render("Max Rally Time : "+timeStr2,True,WHITE,BLACK)
        rallytimeboard_rect = rallytimeboard.get_rect()
        rallytimeboard_rect.x = 15
        rallytimeboard_rect.y = 30
        
        genBoard = genFont.render("Generation: "+str(generation),True,WHITE,BLACK)
        genBoard_rect = genBoard.get_rect()
        genBoard_rect.x = 15
        genBoard_rect.y = 50
        
        mainWindow.fill(BLACK)
        mainWindow.blit(scoreBoard,scoreBoard_rect)
        mainWindow.blit(relaytimeboard,relaytimeboard_rect)
        mainWindow.blit(rallytimeboard,rallytimeboard_rect)
        mainWindow.blit(genBoard,genBoard_rect)
    
        sprites.draw(mainWindow)
        paddle1.move()
        paddle2.move()
        ball.move()
        ball.changeDirection(surface_rect.bottom)
        paddleHit = paddleHit+ paddle_ballHit(paddle1,paddle2,ball)
        pg.display.update()
        if p1_Score ==3 or p2_Score==3:
            return relayTime,rallyTime,(p1_Score+p2_Score)
        
        
        
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
    geneticAlgorithm(mainWindow,surface_rect,clock)
    #playGame(mainWindow,surface_rect,clock)
if __name__ =='__main__':
    pg.init()
    main()
