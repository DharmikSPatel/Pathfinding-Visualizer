from io import TextIOWrapper
from math import inf
from node import Node

from queue import PriorityQueue

import pygame as pygame
from pygame import font,display,draw,time
from pygame.time import Clock
from pygame.locals import *

from pygame_widgets import Button

pygame.init()
screen = display.set_mode([1000, 900])
EMPTY_COLOR = "gray"
BACKGROUND_COLOR = (37, 59, 89)
STARTING_NODE_COLOR = (191, 60, 31)
ENDING_NODE_COLOR = (57, 115, 77)
PATH_COLOR = (242, 197, 61)
WALL_COLOR = (8, 27, 38)
LINE_COLOR = "white"
OPEN_NODE_COLOR = (217, 113, 151)
CLOSED_NODE_COLOR = (91, 123, 166)
font1: font.Font = font.SysFont("Arial", 15)



maze = []

def createMazeFromFile(fileName: str):
    with open(fileName, "r") as mazeFile:
        maxRow: int = 0
        maxCol: int = 0
        for line in mazeFile:
            maze.append([])
            maxCol = len(line)
            for x in range(maxCol):
                letter: str = line[x]
                if letter == "*":
                    maze[maxRow].append(Node(x, maxRow, EMPTY_COLOR, Node.TYPE_EMPTY))
                elif letter == "w":
                    maze[maxRow].append(Node(x, maxRow, WALL_COLOR, Node.TYPE_WALL))
                elif letter == "s":
                    maze[maxRow].append(Node(x, maxRow, STARTING_NODE_COLOR, Node.TYPE_START))
                elif letter == "e":
                    maze[maxRow].append(Node(x, maxRow, ENDING_NODE_COLOR, Node.TYPE_END))
            maxRow+=1
        Node.SIZE = int(1000/max(maxRow, maxCol))
        Node.X_OFFSET = int((1000-(Node.SIZE*maxCol))/2)
        for row in maze:
            for node in row:
                node.setUpRect()

def createMaze(x, y, r, c, start, end):  
    for i in range(r):
        maze.append([])
        for j in range(c):
            color = EMPTY_COLOR
            type = Node.TYPE_EMPTY
            if (i, j) == start:
                color = STARTING_NODE_COLOR
                type = Node.TYPE_START
            elif (i, j) == end:
                color = ENDING_NODE_COLOR
                type = Node.TYPE_END
            maze[i].append(Node(j, i, color, type))

def drawMaze():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            draw.rect(screen, maze[i][j].color, maze[i][j].rect)
            #imgFont = font1.render(f" {maze[i][j].getGCost()}+{maze[i][j].getHCost()}={str(maze[i][j].getFCost()) + maze[i][j].getArrow()}", True, WHITE)
            #screen.blit(imgFont, maze[i][j].rect)
    
    start = 0
    end = len(maze)*Node.SIZE
    for i in range(len(maze[0])+1):
        draw.line(screen, LINE_COLOR, (Node.SIZE*i+Node.X_OFFSET, start), (Node.SIZE*i+Node.X_OFFSET, end))
    
    start = +Node.X_OFFSET
    end = len(maze[0])*Node.SIZE+Node.X_OFFSET
    for i in range(len(maze)+1):
        draw.line(screen, LINE_COLOR, (start, Node.SIZE*i), (end, Node.SIZE*i))
    

createMazeFromFile("maze.txt")
open = PriorityQueue() #all the nodes that r looked at
open.put(Node.START_NODE)
closed = [] #currnt path list, more exlcuisve, so all the nodes that cause expansion



startButton = Button(screen, 700, 20, 100, 40, text="Start", onClick=lambda : print("clicked"))
stepSpeed = 0
stepThreshold = 0

def events() -> bool:
    stop = False
    gameEvents = pygame.event.get()
    for event in gameEvents:
        if event.type == pygame.QUIT:
            stop = True
    startButton.listen(gameEvents)

    return not stop

def drawMenu():
    startButton.draw()



def Astar() -> bool:
    bestNode: Node = open.get(timeout=1)
    bestNode.color = CLOSED_NODE_COLOR if bestNode.type != Node.TYPE_START else STARTING_NODE_COLOR
    closed.append(bestNode)
    if bestNode is Node.END_NODE:
        for row in maze:
            for node in row:
                if node.type == Node.TYPE_EMPTY:
                    node.color = EMPTY_COLOR
        bestNode.highlightPath(PATH_COLOR, STARTING_NODE_COLOR, ENDING_NODE_COLOR)
        return True
    for i in range(max(bestNode.y-1, 0), min(bestNode.y+2, len(maze))):
        for j in range(max(bestNode.x-1, 0), min(bestNode.x+2, len(maze[i]))):
            curNode: Node = maze[i][j]
            if curNode is bestNode or curNode in closed or curNode.type == Node.TYPE_WALL:
                continue
            curNode.color = OPEN_NODE_COLOR
            if curNode in open.queue:
                tempParrent: Node = curNode.parrent
                tempGCost: int = curNode.getGCost()
                curNode.parrent = bestNode
                if tempGCost < curNode.getGCost():
                    curNode.parrent = tempParrent
                else:
                    open.put(open.get())
            else:
                curNode.parrent = bestNode
                open.put(curNode)
    return False
    
                
                
gameClock = Clock()

running: bool = True
winnerFound: bool = False
while running:
    running = events()

    
    screen.fill(BACKGROUND_COLOR)

    drawMenu()

    if time.get_ticks() >= stepThreshold:
        if not winnerFound:
            winnerFound = Astar()
        if winnerFound:
            pass
        stepThreshold+=stepSpeed
    
    drawMaze()
    pygame.display.flip()
    #gameClock.tick(30)
    
pygame.quit()
