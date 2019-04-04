import pygame
import numpy as np
import random
pygame.init()

class MAZE:
    alg=1
    xres = 50
    yres = 50
    colways = (0,0,0)
    colwalls = (128,128,128)
    colrightway = (200,200,200)
    StartRes = 700
    displayresx = StartRes
    displayresy = StartRes
    recx=(displayresx / xres)
    recy=(displayresy / yres)
    cellx = int((recx) * 0.8)
    celly = int((recy) * 0.8)
    Maze = np.zeros((yres+2, xres+2), dtype = bool)
    Maze[:, :] = True
    Maze[1 : yres + 1, 1 : xres + 1] = False
    MazeWay=[]
    MazeField=pygame.display.set_mode((displayresx,displayresy))
    MazeField.fill(colwalls)
    def Update(self):
        self.recx=(self.displayresx / self.xres)
        self.recy=(self.displayresy / self.yres)
        self.cellx = int((self.recx) * 0.8)
        self.celly = int((self.recy) * 0.8)
        self.Maze = np.zeros((self.yres+2, self.xres+2), dtype = bool)
        self.Maze[:, :] = True
        self.Maze[1 : self.yres + 1, 1 : self.xres + 1] = False
        self.MazeWay=[]
        self.MazeField=pygame.display.set_mode((self.displayresx,self.displayresy))
        self.MazeField.fill(self.colwalls)
        pygame.display.update()
    def SetXres(self,x):
        if x*16>self.StartRes:
            self.displayresx = self.StartRes
        else :
            self.displayresx = x * 16
        self.xres=x
    def SetYres(self,x):
        if x*16>self.StartRes:
            self.displayresy = self.StartRes
        else:
            self.displayresy = x * 16
        self.yres=x





def Coord(point,M):
    return (int(point[0]*M.recy) - (M.celly+M.recy) / 2, int(point[1] * M.recx) - (M.cellx + M.recx) / 2)


def DrowConnection(point1,point2,M,color):

    pygame.time.delay(2)
    col = color
    dx=point1[1]-point2[1]
    dy=point1[0]-point2[0]
    (y,x)=Coord(point1,M)
    pygame.draw.rect(M.MazeField,col,(x,y,M.cellx,M.celly))
    (y,x)=Coord(point2,M)
    pygame.draw.rect(M.MazeField,col,(x,y,M.cellx,M.celly))
    x=x+dx*M.recx/2
    y=y+dy*M.recy/2
    pygame.draw.rect(M.MazeField,col,(x,y,M.cellx,M.celly))

def FindAWayOut(M):
    now=(M.yres,M.xres)

    while now != (1,1):
        back = StepBack(now,M)
        DrowConnection(now,back,M,M.colrightway)
        pygame.display.update()
        now=back

    while now != (1,1) :
        back = StepBack(now,M)
        DrowConnection(back,now,M,M.colrightway)
        pygame.display.update()
        now=back

def InitMaze(M):
    if(M.alg == 1):
        InitMazeDFS(M)
    else:
        InitMazePrim(M)
    DrowMaze(M)

def DrowMaze(M):


    M.MazeField.fill(M.colwalls)

    for i in range(1, M.yres + 1 ):
        for j in range(1, M.xres + 1):
            (y, x)=Coord((i, j),M)
            pygame.draw.rect(M.MazeField,(128,128,128),(x, y, M.cellx, M.celly))

    for i in M.MazeWay:
        DrowConnection(i[0],i[1],M,M.colways)
        pygame.display.update()
    WriteMaze(M)

def FindFriends(point,M):
    UnVisited=[]
    x=point[0]
    y=point[1]
    if not M.Maze[x+1,y]:
        UnVisited+=[(x+1,y)]
    if not M.Maze[x-1,y]:
        UnVisited+=[(x-1,y)]
    if not M.Maze[x,y-1]:
        UnVisited+=[(x,y-1)]
    if not M.Maze[x,y+1]:
        UnVisited+=[(x,y+1)]
    return UnVisited


def StepBack(point,M):

    for i in M.MazeWay:
        if i[0] == point:
            return i[1]
    return []

def InitMazeDFS(M):
    M.Maze[:, :] = True
    M.Maze[1 : M.yres + 1, 1 : M.xres + 1] = False
    now=(1,1)
    M.Maze[now]=True
    Friends=FindFriends(now,M)

    second=random.choice(Friends)

    M.Maze[second]=True

    M.MazeWay=[(second,now)]
    now=second
    back=StepBack(now,M)
    while (back != []):
        Friends=FindFriends(now,M)
        while Friends != []:
            second=random.choice(Friends)
            M.Maze[second]=True
            M.MazeWay+=[(second,now)]
            now=second
            Friends=FindFriends(now,M)
        now=StepBack(now,M)
        back=StepBack(now,M)




def InitMazePrim(M):

    M.Maze[:, :] = True
    M.Maze[1 : M.yres + 1, 1 : M.xres + 1] = False
    M.MazeWay=[]
    walls=set()
    now=(1,1)
    Friends=FindFriends(now,M)
    M.Maze[now]=True
    for i in Friends:
        walls.add((i,now))
    while len(walls) != 0:
        wall=random.choice(list(walls))
        if M.Maze[wall[0]]:
            walls.discard(wall)
        else:
            now=wall[0]
            Friends=FindFriends(now,M)
            M.Maze[now]=True
            for i in Friends:
                walls.add((i,now))
            M.MazeWay+=[wall]



def ReadMaze(M):
    M.MazeWay=[]
    file=open("LastM.Maze.txt","r")
    lines=file.readlines()
    for i in lines:
        n = i.split(' ')
        M.MazeWay+=[((int(n[0]),int(n[1])),(int(n[2]),int(n[3])))]
    file.close();
    DrowMaze(M)

def WriteMaze(M):
    file=open("LastM.Maze.txt","w")
    for i in M.MazeWay:
        file.write(str(i[0][0])+" "+str(i[0][1])+" "+str(i[1][0])+" "+str(i[1][1])+"\n")
    file.close()





run = True
M=MAZE()
print("Hello!\n Press Q or E to switch mod\nPress W to read last M.Maze\nPress SPACE to Start Drawing\nPress F to draw right way\nA to set resolution\nEnjoy!")
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        M.alg=1
    if keys[pygame.K_q]:
        M.alg=2
    if keys[pygame.K_w]:
        ReadMaze(M)
    if keys[pygame.K_a]:
        print("input X resolution of Maze")
        x=int(input())
        M.SetXres(x)
        print("input Y resolution of Maze")
        x=int(input())
        M.SetYres(x)
        M.Update()
    if keys[pygame.K_f]:
        if len(M.MazeWay) == 0:
            InitM.Maze(M)
        FindAWayOut(M)
    if keys[pygame.K_SPACE]:
        InitMaze(M)

pygame.quit()
