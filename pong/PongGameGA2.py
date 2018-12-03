# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 21:12:09 2018

@author: nikhi
"""

import pygame as pg
import sys
import time
import numpy as np
from pygame.locals import *
from random import randint
from random import uniform
from random import shuffle
import matplotlib.pyplot as plt 


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

#Game Generation
GAME_GENERATION1 = 0
GAME_GENERATION2 = 0

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

BESTCHROMOSOMEP1 = [0.99,0.1,0.9,0.0,0.0,0.1]

BESTCHROMOSOMEP2 = [0.0,0.0,0.1,0.99,0.1,0.9]
#fonts 
score_font = None

#Graph axism list
xMAGeneration=[]
yMAavgFitness=[]

xGAGeneration=[]
yGAavgFitness=[]

def plotGraph(x1,y1,x2,y2,title,xaxis,yaxis):
    plt.plot(x1, y1,'-b',label='GA')
    #title = "Leaning Curve with HyperParameters"
    plt.plot(x2,y2,'-r',label='MA')
    plt.legend() 
    plt.xlabel(xaxis)
    plt.ylabel(yaxis) 
    plt.title(title)
    plt.show() 




def getRandomGene():
    num = randint(0,5)
    gene=[0.0,0.0,0.0,0.0,0.0,0.0]
    for i in range(num):
        j = randint(0,5)
        gene[j]=round(uniform(0,1),2)
        
    #gene =[round(uniform(0,1),2),round(uniform(0,1),2),round(uniform(0,1),2),round(uniform(0,1),2),round(uniform(0,1),2),round(uniform(0,1),2)]
    return gene
    
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
        self.hit = 0
        self.distance=0
        self.gene=getRandomGene()
        self.relayTime =0.0
        self.rallyTime = 0.0
        self.image = pg.Surface([10,100])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.speed = 7
        self.fitness = 0
        # Paddle Location
        if self.playerID ==0:
            self.rect.centerx = self.xleft
            self.rect.centerx +=50
        elif self.playerID ==1:
            self.rect.centerx = self.xright
            self.rect.centerx -=50
        self.rect.centery = self.centery
    def calculateFitness(self):
        self.fitness = (((self.relayTime+0.1)/(self.rallyTime+0.1))*self.hit)+self.distance
        #print(self.fitness)
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
                self.distance+=self.speed
            elif (MOVE_DOWN1==True) and (self.rect.bottom <WINDOW_HEIGHT-5):
                self.rect.y +=self.speed
                self.distance+=self.speed
            elif (NO_MOVE1==True):
                pass
            
        if self.playerID == 1:
            if (MOVE_UP2==True) and (self.rect.y>5):
                
                self.rect.y -=self.speed
                self.distance+=self.speed
            elif (MOVE_DOWN2==True) and (self.rect.bottom <WINDOW_HEIGHT-5):
                self.rect.y +=self.speed
                self.distance+=self.speed
            elif (NO_MOVE2==True):
                pass
    def autoMove(self,bx,by):
        p1 = self.gene[0]
        c1 = self.gene[1]
        c2 = self.gene[2]
        p2 = self.gene[3]
        c3 = self.gene[4]
        c4 = self.gene[5]
        x = self.rect.x - bx 
        y = self.rect.y - by
        number1 = uniform(0,1)
        number2 = uniform(0,1)
        if number1 < p1: 
            if x < 0 and y < 0:
                getMove(1,c1)
                #print("moving for -x -y","px: ",px," py: ",py," bx: ",bx," by:",by)
            elif x < 0 and y > 0:
                getMove(1,c2)
                #print("moving for -x +y","px: ",px," py: ",py," bx: ",bx," by:",by)
        if number2 < p2:
            if x > 0 and y < 0:
                getMove(2,c3)
                #print("moving for +x -y","px: ",px," py: ",py," bx: ",bx," by:",by)
            elif x > 0 and y >0:
                getMove(2,c4)
                #print("moving for +x +y","px: ",px," py: ",py," bx: ",bx," by:",by)
        
def paddle_ballHit(paddle1,paddle2,ball):
    if pg.sprite.collide_rect(ball,paddle2):
        if ball.direction == FWD_RIGHT:
            ball.direction = FWD_LEFT
        elif ball.direction ==BWD_RIGHT:
            ball.direction = BWD_LEFT
        ball.speed *= 1.01
        paddle2.hit+=1
    if pg.sprite.collide_rect(ball,paddle1):
        if ball.direction == FWD_LEFT:
            ball.direction = FWD_RIGHT
        elif ball.direction ==BWD_LEFT:
            ball.direction = BWD_RIGHT
        ball.speed *= 1.01
        paddle1.hit+=1

def Evaluate1(P1,bp2,mainWindow,surface_rect,clock):
    p1 = P1
    p2 = bp2
    currentFitness = 0
    for i in range(0,5):
        
        flag,relayTime,rallyTime = playGame(mainWindow,surface_rect,clock,p1,p2,i,0,True,GAME_GENERATION2)
        if flag==False:
            return p1
        else:
            p1.relayTime = relayTime
            p1.rallyTime = rallyTime
            p1.calculateFitness()
            myfitness = p1.fitness
            if myfitness<currentFitness:
                return p1
            else:
                p1.gene = mutate(p1.gene,1)
                currentFitness = myfitness
    return p1

def Evaluate2(bp1,P2,mainWindow,surface_rect,clock):
    p2 = P2
    p1 = bp1
    currentFitness = 0
    for i in range(0,5):
        
        flag,relayTime,rallyTime = playGame(mainWindow,surface_rect,clock,p1,p2,i,0,True,GAME_GENERATION2)
        if flag==True:
            return p2
        else:
            p2.relayTime = relayTime
            p2.rallyTime = rallyTime
            p2.calculateFitness()
            myfitness = p2.fitness
            if myfitness<currentFitness:
                return p2
            else:
                p2.gene = mutate(p2.gene,1)
                currentFitness = myfitness
    return p2
def getAvgFitness(pop1,pop2):
    sum1=sum([x.fitness for x in pop1])
    sum2 = sum([x.fitness for x in pop2])
    avg = (sum1+sum2)/(len(pop1)+len(pop2))
    return avg
def MA(mainWindow,surface_rect,clock,pop1,pop2):
    global GAME_GENERATION2
    SIZE = 10
    paddle1population=pop1
    paddle2population=pop2
    for i in range(len(pop1)):
        p1 = paddle1population[i]
        bp2 = Paddle(1,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
        bp2.gene = BESTCHROMOSOMEP2
        p1 = Evaluate1(p1,bp2,mainWindow,surface_rect,clock)
        paddle1population[i] = p1
       
        p2 = paddle2population[i]
        bp1 = Paddle(0,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
        bp1.gene = BESTCHROMOSOMEP1
       
        p2 = Evaluate2(bp1,p2,mainWindow,surface_rect,clock)
        paddle2population[i]= p2
    i=0
    j=0
    maxRelayTime = 0.0
    while maxRelayTime < 1000.0 and GAME_GENERATION2<40:
        
        f,relayTime,rallyTime,num= doTask(mainWindow,surface_rect,clock,paddle1population,paddle2population,i,j,GAME_GENERATION2)
        if relayTime> maxRelayTime:
            maxRelayTime = relayTime
        if f==False:
            i=0
            j=num
            paddle1population = doCrossoverMutations(paddle1population)
            for i in range(0,len(paddle1population)-6):
                bp2 = Paddle(1,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
                bp2.gene = BESTCHROMOSOMEP2
                paddle1population[i] = Evaluate1(paddle1population[i],bp2,mainWindow,surface_rect,clock)
        
        if f==True:
            j=0
            i=num
            paddle2population=doCrossoverMutations(paddle2population)
            for i in range(0,len(paddle1population)-6):
                p2 = Paddle(1,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
                bp1 = Paddle(0,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
                bp1.gene = BESTCHROMOSOMEP1
                p2 = Evaluate2(bp1,p2,mainWindow,surface_rect,clock)
 
        xMAGeneration.append(GAME_GENERATION2)
        GAME_GENERATION2+=1
        avg = getAvgFitness(paddle1population,paddle2population)
        yMAavgFitness.append(avg)
        print("MA avg Fitness: ",avg)
    print("done")

def GA(mainWindow,surface_rect,clock,pop1,pop2):
    global GAME_GENERATION1
    paddle1population=pop1
    paddle2population=pop2
    i=0
    j=0
    maxRelayTime = 0.0
    while maxRelayTime < 1000.0 and GAME_GENERATION1<20:
        
        f,relayTime,rallyTime,num= doTask(mainWindow,surface_rect,clock,paddle1population,paddle2population,i,j,GAME_GENERATION1)
        if relayTime> maxRelayTime:
            maxRelayTime = relayTime
        if f==False:
            i=0
            j=num
            paddle1population = doCrossoverMutations(paddle1population)
            
        if f==True:
            j=0
            i=num
            paddle2population=doCrossoverMutations(paddle2population)
        xGAGeneration.append(GAME_GENERATION1)
        GAME_GENERATION1+=1
        avg = getAvgFitness(paddle1population,paddle2population)
        yGAavgFitness.append(avg)
        print("GA avg Fitness: ",avg)
    print("done")
def doTask(mainWindow,surface_rect,clock,pad1List,pad2List,i,j,gg):
    while i<len(pad1List) and j<len(pad2List):
        p1=pad1List[i]
        p2=pad2List[j]
        flag,relayTime,rallyTime = playGame(mainWindow,surface_rect,clock,p1,p2,i,j,False,gg)
        
        if flag == False:
            pad2List[j].relayTime = relayTime
            pad2List[j].rallyTime = rallyTime
            pad2List[j].calculateFitness()
            j+=1
        if flag ==True:
            pad1List[i].relayTime = relayTime
            pad1List[i].rallyTime = rallyTime
            pad1List[j].calculateFitness()
            i+=1
    if i ==len(pad1List):
        return False,relayTime,rallyTime,j
    if j ==len(pad2List):
        return True,relayTime,rallyTime,i


def doCrossoverMutations(padlist):
    padlist = sorted(padlist,key=getKey)
    padlist1 = padlist[:6]
    padlist2 = padlist[6:]
    for i in range(0,len(padlist1),2):
        point = randint(1,5)
        f1 = padlist1[i].gene[:point]
        b1 = padlist1[i].gene[point:]
        
        f2 = padlist1[i+1].gene[:point]
        b2 = padlist1[i+1].gene[point:]
        x = randint(0,1)
        if x==1:
            padlist1[i].gene = f1+b2
            padlist1[i+1].gene= f2+b1
        if x==0:
            padlist1[i].gene = f2+b1
            padlist1[i+1].gene= f1+b2
        padlist1[i].gene = mutate(padlist1[i].gene,0.6)
        padlist1[i+1].gene= mutate(padlist1[i+1].gene,0.6)
        padlist1[i].rect.centery =padlist1[i].centery
        padlist1[i+1].rect.centery =padlist1[i+1].centery
    padlist = padlist1 + padlist2
    return padlist

def mutate(gene,prob):
    
    num = uniform(0,1)
    if num<prob:
        pos = randint(0,len(gene)-1)
        gene[pos] = round(uniform(0,1),2)
    return gene        
                
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
    
    
    
def getKey(paddle):
        return paddle.fitness
    
    
    
    
    
#Game Play
def playGame(mainWindow,surface_rect,clock,p1,p2,i,j,evaluate,GAME_GENERATION):
    paddle1 = p1
    paddle2 = p2
    ball = Ball(surface_rect.centerx,surface_rect.centery)
    sprites = pg.sprite.RenderPlain(paddle1,paddle2,ball)
    p1_Score = 0
    p2_Score = 0
    score_font = pg.font.SysFont("Helvetica",100)
    timeFont  =pg.font.SysFont("Helvetica",20)
    timeFont2  =pg.font.SysFont("Helvetica",20)
    gen1 = pg.font.SysFont("Helvetica",10)
    gen2 = pg.font.SysFont("Helvetica",10)
    
    gameItr = pg.font.SysFont("Helvetica",20)
    
    pgen1 = pg.font.SysFont("Helvetica",10)
    pgen2 = pg.font.SysFont("Helvetica",10)
    
    evalFont = pg.font.SysFont("Helvetica",10)
    
    
    startTime = time.time()
    rstartTime = time.time()
    rallyTime = 0.00
    
    count =0
    while True:
        clock.tick(300)
        
        if ball.rect.x >WINDOW_WIDTH:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(0,1)
            ball.speed = 4
            p1_Score+=1
            rstartTime = time.time()
        elif ball.rect.x<0:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(2,3)
            ball.speed = 4
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
        
        if evaluate ==True:
            evalBoard=evalFont.render("Evaluating the Paddle",True,WHITE,BLACK)
            evalBoard_rect=evalBoard.get_rect()
            evalBoard_rect.x = surface_rect.centerx
            evalBoard_rect.y = surface_rect.centery
            
        relaytimeboard = timeFont.render("Relay Time : "+timeStr,True,WHITE,BLACK)
        relaytimeboard_rect = relaytimeboard.get_rect()
        relaytimeboard_rect.x = 15
        relaytimeboard_rect.y = 10
        
        
        rallytimeboard = timeFont2.render("Max Rally Time : "+timeStr2,True,WHITE,BLACK)
        rallytimeboard_rect = rallytimeboard.get_rect()
        rallytimeboard_rect.x = 15
        rallytimeboard_rect.y = 30
        
        gen1board = gen1.render("Paddle Generation: "+str(j),True,WHITE,BLACK)
        gen1board_rect = gen1board.get_rect()
        gen1board_rect.x = WINDOW_WIDTH-180
        gen1board_rect.y = 50
        
        gameITRboard = gameItr.render("Generation: "+str(GAME_GENERATION),True,WHITE,BLACK)
        gameITRboard_rect = gameITRboard.get_rect()
        gameITRboard_rect.x = surface_rect.centerx
        gameITRboard_rect.y = 5
        
        pgen1board = pgen1.render("gene: "+str(paddle1.gene),True,WHITE,BLACK)
        pgen1board_rect = pgen1board.get_rect()
        pgen1board_rect.x = 10
        pgen1board_rect.y = 60
        
        pgen2board = pgen2.render("gene: "+str(paddle2.gene),True,WHITE,BLACK)
        pgen2board_rect = pgen2board.get_rect()
        pgen2board_rect.x = WINDOW_WIDTH-180
        pgen2board_rect.y = 60
        
        
        gen2board = gen2.render("Paddle Generation: "+str(i),True,WHITE,BLACK)
        gen2board_rect = gen2board.get_rect()
        gen2board_rect.x = 10
        gen2board_rect.y = 50
        
        
        mainWindow.fill(BLACK)
        mainWindow.blit(scoreBoard,scoreBoard_rect)
        mainWindow.blit(relaytimeboard,relaytimeboard_rect)
        mainWindow.blit(rallytimeboard,rallytimeboard_rect)
        mainWindow.blit(gen1board,gen1board_rect)
        mainWindow.blit(gen2board,gen2board_rect)
        mainWindow.blit(pgen1board,pgen1board_rect)
        mainWindow.blit(pgen2board,pgen2board_rect)
        mainWindow.blit(gameITRboard,gameITRboard_rect)
        
        if evaluate==True:
            mainWindow.blit(evalBoard,evalBoard_rect)
        
        sprites.draw(mainWindow)
        paddle1.autoMove(ball.rect.x,ball.rect.y)
        paddle2.autoMove(ball.rect.x,ball.rect.y)
        
        paddle1.move()
        paddle2.move()
        ball.move()
        ball.changeDirection(surface_rect.bottom)
        paddle_ballHit(paddle1,paddle2,ball)
        pg.display.update()
        if evaluate ==True:
            if  p1_Score == 1:
                return False,relayTime,rallyTime
            if p2_Score == 1:
                return True,relayTime,rallyTime
        
        if  p1_Score == 3:
            return False,relayTime,rallyTime
        if p2_Score == 3:
            return True,relayTime,rallyTime
        
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
    pop1 =[]
    pop2 =[]
    SIZE=10
    for i in range(SIZE):
        p1 = Paddle(0,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
        pop1.append(p1)
        p2 = Paddle(1,mainWindow.get_rect().left,mainWindow.get_rect().right,mainWindow.get_rect().centery)
        pop2.append(p2)
    GA(mainWindow,surface_rect,clock,pop1,pop2)
    MA(mainWindow,surface_rect,clock)
    plotGraph(xGAGeneration,yGAavgFitness,xMAGeneration,yMAavgFitness,"GA vs MA","Generations","Avg reward")
if __name__ =='__main__':
    pg.init()
    main()