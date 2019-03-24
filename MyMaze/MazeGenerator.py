import pygame
import numpy as np
import random
pygame.init()

alg=1
xres = 50
yres = 50
col1 = (0,0,0)
col2 = (128,128,128)
col3 = (255,255,255)
displayresx = 800
displayresy = 800
recx=(displayresx / xres)
recy=(displayresy / yres)
cellx = int((recx) * 0.8)
celly = int((recy) * 0.8)
Maze = np.zeros((yres+2, xres+2), dtype = bool)
Maze[:, :] = True
Maze[1 : yres + 1, 1 : xres + 1] = False
MazeWay=[]
MazeField=pygame.display.set_mode((displayresx,displayresy))
MazeField.fill(col1)
pygame.display.update()


def Coord(point):
    return (int(point[0]*recy) - (celly+recy) / 2, int(point[1] * recx) - (cellx + recx) / 2)


def DrowConnection(point1,point2,color=1):

    pygame.time.delay(5)
    col = col2

    if(color != 1):
        col = col3
    dx=point1[1]-point2[1]
    dy=point1[0]-point2[0]
    (y,x)=Coord(point1)
    pygame.draw.rect(MazeField,col,(x,y,cellx,celly))
    (y,x)=Coord(point2)
    pygame.draw.rect(MazeField,col,(x,y,cellx,celly))
    x=x+dx*recx/2
    y=y+dy*recy/2
    pygame.draw.rect(MazeField,col,(x,y,cellx,celly))

def FindAWayOut(Start=(1,1),End=(yres,xres)):
    global MazeWay
    global Maze
    global MazeField
    now=End
    while now != (1,1) and now != Start:
        back = StepBack(now)
        DrowConnection(now,back,2)
        pygame.display.update()
        now=back
    if(now != Start):
        now=Start
        while now != (1,1) :
            back = StepBack(now)
            DrowConnection(back,now,2)
            pygame.display.update()
            now=back

def InitMaze():
    if(alg == 1):
        InitMazeDFS()
    else:
        InitMazePrim()
    DrowMaze()

def DrowMaze():

    global MazeWay
    global Maze
    global MazeField

    MazeField.fill(col1)

    for i in range(1, yres + 1 ):
        for j in range(1, xres + 1):
            (y, x)=Coord((i, j))
            pygame.draw.rect(MazeField,(128,128,128),(x, y, cellx, celly))

    for i in MazeWay:
        DrowConnection(i[0],i[1])
        pygame.display.update()
    WriteMaze()

def FindFriends(point):
    global MazeWay
    global Maze
    UnVisited=[]
    x=point[0]
    y=point[1]
    if not Maze[x+1,y]:
        UnVisited+=[(x+1,y)]
    if not Maze[x-1,y]:
        UnVisited+=[(x-1,y)]
    if not Maze[x,y-1]:
        UnVisited+=[(x,y-1)]
    if not Maze[x,y+1]:
        UnVisited+=[(x,y+1)]
    return UnVisited


def StepBack(point):
    global MazeWay
    for i in MazeWay:
        if i[0] == point:
            return i[1]
    return []

def InitMazeDFS():
    global MazeWay
    global Maze
    Maze[:, :] = True
    Maze[1 : yres + 1, 1 : xres + 1] = False
    now=(1,1)
    Maze[now]=True
    Friends=FindFriends(now)

    second=random.choice(Friends)

    Maze[second]=True

    MazeWay=[(second,now)]
    now=second
    back=StepBack(now)
    while (back != []):
        Friends=FindFriends(now)
        while Friends != []:
            second=random.choice(Friends)
            Maze[second]=True
            MazeWay+=[(second,now)]
            now=second
            Friends=FindFriends(now)
        now=StepBack(now)
        back=StepBack(now)




def InitMazePrim():
    global MazeWay
    global Maze
    Maze[:, :] = True
    Maze[1 : yres + 1, 1 : xres + 1] = False
    MazeWay=[]
    walls=set()
    now=(1,1)
    Friends=FindFriends(now)
    Maze[now]=True
    for i in Friends:
        walls.add((i,now))
    while len(walls) != 0:
        wall=random.choice(list(walls))
        if Maze[wall[0]]:
            walls.discard(wall)
        else:
            now=wall[0]
            Friends=FindFriends(now)
            Maze[now]=True
            for i in Friends:
                walls.add((i,now))
            MazeWay+=[wall]



def ReadMaze():
    global MazeWay
    global Maze
    MazeWay=[]
    file=open("LastMaze.txt","r")
    lines=file.readlines()
    for i in lines:
        n = i.split(' ')
        MazeWay+=[((int(n[0]),int(n[1])),(int(n[2]),int(n[3])))]
    file.close();
    DrowMaze()

def WriteMaze():
    global MazeWay
    global Maze
    file=open("LastMaze.txt","w")
    for i in MazeWay:
        file.write(str(i[0][0])+" "+str(i[0][1])+" "+str(i[1][0])+" "+str(i[1][1])+"\n")
    file.close()





run = True
print("Hello!\n Press Q or E to switch mod\nPress W to read last Maze\nPress SPACE to Start Drawing\nPress F to draw right way\nEnjoy!")
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        alg=1
    if keys[pygame.K_q]:
        alg=2
    if keys[pygame.K_w]:
        ReadMaze()
    if keys[pygame.K_f]:
        if len(MazeWay) == 0:
            InitMaze()
        FindAWayOut()
    if keys[pygame.K_SPACE]:
        InitMaze()

pygame.quit()
