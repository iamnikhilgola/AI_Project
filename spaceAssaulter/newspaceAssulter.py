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
SHOOT = False

#Bullet speed
BSPEED = 10


#Color Vairables 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

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
       
def getMove(c):
    if c>=0.0 and c<0.3:
        moveDown(playerID)
    elif c >=0.3 and c <0.7:
        noMove(playerID)
    elif c >=0.7 and c <= 1:
        moveUp(playerID)
        
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
    
    
    def moveAll(self,PLEFT,PRIGHT,NOMOVE,SHOOT):
        #global PLEFT
        #global PRIGHT
        #global NOMOVE
        #global SHOOT
        if (PLEFT == True) and (self.rect.x>5):
            self.rect.x -=self.speed
        elif (PRIGHT == True) and (self.rect.x < WINDOW_WIDTH -25):
            self.rect.x += self.speed
        elif (SHOOT == True):
            newBullet =Bullet(self.rect.x,self.rect.y)
            newBullet.update()
            return newBullet
        else: # NOMOVE is True
            pass
        
    def move(self,option):
        if option == 1:
            PLEFT = True
            PRIGHT = False
            NOMOVE = False
            SHOOT = False
            self.moveAll(PLEFT,PRIGHT,NOMOVE,SHOOT)           
        elif option ==2:
            PLEFT = False
            PRIGHT = True
            NOMOVE = False
            SHOOT = False
            self.moveAll(PLEFT,PRIGHT,NOMOVE,SHOOT) 
        elif option ==3:
            PLEFT = False
            PRIGHT = False
            NOMOVE = True
            SHOOT = False
            self.moveAll(PLEFT,PRIGHT,NOMOVE,SHOOT) 
        elif option ==4:
            PLEFT = False
            PRIGHT = False
            NOMOVE = False
            SHOOT = True
            bullet=self.moveAll(PLEFT,PRIGHT,NOMOVE,SHOOT)
            return bullet
        else:
            pass
        
    
    def automove(self,chromosome,rangeValue):
        if chromosome[0] <= 0.33:
            self.move(1)
        elif chromosome[1]>0.33 and chromosome[1]<=0.67:
            self.move(2)
        elif chromosome[2]>0.67 and chromosome[2]<=1:
            self.move(3)
        elif chromosome[3]>0.1 and (rangeValue-chromosome[4])>0:
            bullet =self.move(4)
            return bullet
        elif chromosome[4]>0.5:
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
            if self.rect.y<30:
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
    #time1-=time.time()
    time2 = max(timeArray)#-time.time()
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

def health_bars(rocket_health,gameWindow):
    if rocket_health > 75:
        rocket_health_color = GREEN
    if rocket_health >50:
        rocket_health_color = YELLOW
    elif rocket_health < 50 and rocket_health>0:
        rocket_health_color = RED
    else:
        return 0

    pg.draw.rect(gameWindow , rocket_health_color,(800,10,rocket_health , 25))

def createPopulation():
    population=[0 for i in range(10)]
    for i in range(10):
        population[i]=chromosome()
    return population

def crossover(chromosome1,chromosome2):
    point = random.randint(1,10)
    child1 = chromosome1[:point]+chromosome2[point:]
    child2 = chromosome2[:point]+chromosome1[point:] 
    return child1,child2

def mutation(chromosome):
    point= random.randint(0,5)
    chromosome[point]=random.random()
    return chromosome
    
def parentSelection(fitnessValues,initialpopulation):
    bestparents=[0,0,0,0,0]
    for i in range(5):
        max1=max(fitnessValues)
        index=fitnessValues.index(max1)
        print(index,initialpopulation[index])
        parent1 = initialpopulation[index]
        initialpopulation.remove(parent1)
        fitnessValues.remove(max1)
        bestparents[i]=parent1
    return bestparents

def calcfitness(score,time):
    return  (0.7*score + 0.3*time)/2

def geneticAlgo_rocket(gameWindow,surface_rect,clock):
    rocket = Rocket(gameWindow.get_rect().bottom,gameWindow.get_rect().centerx,gameWindow.get_rect().centery)
    initialpopulation=createPopulation()
    newspecies =0
    newpopulation=initialpopulation
    while(True):
        initialpopulation=newpopulation
        print(len(initialpopulation))
        fitnessValues = [0 for i in range(10)]
        i=0
        for chromosome in initialpopulation:
            score,time=playGame(gameWindow,surface_rect,clock,chromosome,rocket,i,newspecies)
            fitnessValues[i]=calcfitness(score,time)
            i+=1
        bestparents=parentSelection(fitnessValues,initialpopulation)
        newpopulation=[]
        flag=0
        for i in range(len(bestparents)):
            for j in range(len(bestparents)):
                if i<j and flag==0:
                    child1,child2=crossover(bestparents[i],bestparents[j])
                    newpopulation.append(child1)
                    newpopulation.append(child2)
                    if(len(newpopulation)>=10):
                        flag=1
        
        for i in range(2):
            newpopulation[i]=mutation(newpopulation[i])
        newspecies+=1
        
def playGame(gameWindow,surface_rect,clock,chromosome,rocket,chrome,species):
    #rocket = Rocket(gameWindow.get_rect().bottom,gameWindow.get_rect().centerx,gameWindow.get_rect().centery)
    time1 =time.time()
    rocket_health = 100
    probability =np.linspace(0,1,4)
    EnemyArray =[]
    for i in probability:
        EnemyArray.append(Enemy(gameWindow.get_rect().centerx,gameWindow.get_rect().centery,i))

    counter = 0
    bullets=[]
    Score= 0
    score_font = pg.font.SysFont("Helvetica",20)
    Timett = pg.font.SysFont("Helvetica",20)
    enemy_font = pg.font.SysFont("Helvetica",20)
    
    while True:
        sprites = pg.sprite.RenderPlain(rocket,tuple(EnemyArray),tuple(bullets))
        clock.tick(200)
        newChro=chromosome#()
        #print(newChro)
        hitting=random.random()
        bullet=rocket.automove(newChro,hitting)
        
        if bullet:
            bullets.append(bullet)
            rocket_health -= 5
        for event in pg.event.get():
            if event.type ==QUIT:
                pg.quit()
                sys.exit()
            """if event.type == KEYDOWN:
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
                    rocket_health -= 5 
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
                #if event.key == K_UP:"""
                    
        for fire in bullets:
            fire.update()
            
        gameWindow.fill(BLACK)
        updatedhealth = health_bars(rocket_health,gameWindow)
        
        if updatedhealth==0:
            time2 = time.time()
            ttime = time2 -time1
            return Score,ttime
        
        sprites.draw(gameWindow)
        
        for enemy in EnemyArray:
            enemy.move()
            enemy.changeDirection(counter)
        
        if(counter%5==0):
            for enemy in EnemyArray:
                for secenemy in EnemyArray:
                    if (enemy != secenemy and len(EnemyArray)<=50):
                        maxtime1,maxtime2= getMaxTime(EnemyArray)
                        newEnemy=EnemyBreeding(enemy,secenemy,maxtime1,maxtime2,gameWindow)
            EnemyArray+=newEnemy
        
        
        for enemy in EnemyArray:
            for fire in bullets:
                if pg.sprite.collide_rect(enemy,fire):
                    enemy.kill()
                    fire.kill()
                    Score = Score+10
                    rocket_health += 7
                    EnemyArray.remove(enemy)
                    bullets.remove(fire)
                    break
                
        scoreBoard = score_font.render("Score :" + str(Score),True,WHITE,BLACK)
        scoreBoard_rect = scoreBoard.get_rect()
        scoreBoard_rect.centerx = surface_rect.centerx
        scoreBoard_rect.y = 10
        
        
        maxTimeboard = Timett.render("Max Living Enemy: "+str(maxtime1),True,WHITE,BLACK)
        maxTimeboard_rect = maxTimeboard.get_rect()
        maxTimeboard_rect.x = 10
        maxTimeboard_rect.y = 10
        
        speciesBoard = enemy_font.render("Species:" + str(species),True,WHITE,BLACK)
        speciesBoard_rect = speciesBoard.get_rect()
        speciesBoard_rect.centerx = 85
        speciesBoard_rect.y = 40
        
        chromeBoard = enemy_font.render("population:" + str(chrome),True,WHITE,BLACK)
        chromeBoard_rect = chromeBoard.get_rect()
        chromeBoard_rect.centerx = 85
        chromeBoard_rect.y = 60
        
        enemyBoard = enemy_font.render("Enemy Count:" + str(len(EnemyArray)),True,WHITE,BLACK)
        enemyBoard_rect = enemyBoard.get_rect()
        enemyBoard_rect.centerx = 85
        enemyBoard_rect.y = 80
        
        gameWindow.blit(scoreBoard,scoreBoard_rect)
        gameWindow.blit(maxTimeboard,maxTimeboard_rect)
        gameWindow.blit(enemyBoard,enemyBoard_rect)
        gameWindow.blit(chromeBoard,chromeBoard_rect)
        gameWindow.blit(speciesBoard,speciesBoard_rect)
        
        #rocket.move()
        pg.display.update()
        counter +=1
        if counter ==1000000:
            counter =0
        if(len(EnemyArray)>50):
            time2=time.time()
            ttime=time2-time1
            return Score,ttime
            #sys.exit()
        
        if(len(EnemyArray)==0):
            time2=time.time()
            ttime= time2-time1
            #time.sleep(0.2)
            return Score,ttime
            #sys.exit()
            GameOver = score_font.render("GAME OVER ",True,WHITE,BLACK)
            GameOver_rect = GameOver.get_rect()
            GameOver_rect.centerx = surface_rect.centerx
            GameOver_rect.y = 150
            gameWindow.blit(GameOver,GameOver_rect)            

def chromosome():
    chromosome=[0,0,0,0,0,0]
    #gene[0] #probability of changing direction left
    #gene[1] #probability of changing direction right
    #gene[2] #probability of no move
    #gene[3] #probability of shooting
    #gene[4] #Threshold for range of Rocket to shoot
    #gene[5] #Speed ratio of rocket
    chromosome=[random.random() for x in range(6)]
    return chromosome
                
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
    geneticAlgo_rocket(gameWindow,surface_rect,clock)
    
if __name__=='__main__':
    pg.init()
    main()    