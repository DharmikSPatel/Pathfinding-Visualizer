from io import TextIOWrapper
from pygame import time
from node import Node
import pygame
from pygame import *
from pygame import draw
from queue import PriorityQueue
import time
from pygame.locals import *
from pygame import font
from pygame import display

pygame.init()
screen = display.set_mode([1000, 900])
BACKGROUND_COLOR = (37, 59, 89)
STARTING_NODE_COLOR = (191, 60, 31)
ENDING_NODE_COLOR = (57, 115, 77)
PATH_COLOR = (242, 197, 61)
WALL_COLOR = (8, 27, 38)
WHITE = "white"
OPEN_NODE_COLOR = (217, 113, 151)
CLOSED_NODE_COLOR = (91, 123, 166)
font1: font.Font = font.SysFont("Arial", 15)



maze = []
startingNode = None



def createMazeFromFile(fileName: str):
    with open(fileName, "r") as mazeFile:
        y: int = 0
        for line in mazeFile:
            maze.append([])
            for x in range(len(line)):
                letter: str = line[x]
                if letter == "*":
                    maze[y].append(Node(x, y, BACKGROUND_COLOR, Node.TYPE_EMPTY))
                elif letter == "w":
                    maze[y].append(Node(x, y, WALL_COLOR, Node.TYPE_WALL))
                elif letter == "s":
                    maze[y].append(Node(x, y, STARTING_NODE_COLOR, Node.TYPE_START))
                elif letter == "e":
                    maze[y].append(Node(x, y, ENDING_NODE_COLOR, Node.TYPE_END))
            y+=1

def createMaze(x, y, r, c, start, end):  
    for i in range(r):
        maze.append([])
        for j in range(c):
            color = BACKGROUND_COLOR
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
            imgFont = font1.render(f" {maze[i][j].getGCost()}+{maze[i][j].getHCost()}={str(maze[i][j].getFCost()) + maze[i][j].getArrow()}", True, WHITE)
            screen.blit(imgFont, maze[i][j].rect)
    
    start = 0
    end = len(maze)*Node.SIZE
    for i in range(len(maze[0])):
        draw.line(screen, WHITE, (Node.SIZE*i, start), (Node.SIZE*i, end))
    draw.line(screen, WHITE, (Node.SIZE*(i+1), start), (Node.SIZE*(i+1), end))
    
    start = 0
    end = len(maze[0])*Node.SIZE
    for i in range(len(maze)):
        draw.line(screen, WHITE, (start, Node.SIZE*i), (end, Node.SIZE*i))
    draw.line(screen, WHITE, (start, Node.SIZE*(i+1)), (end, Node.SIZE*(i+1)))
    
    

#createMaze(0, 0, 6, 11, (4, 7), (1, 4))
#createMaze(0, 0, 10, 10, (2, 4), (9, 9))
#createMazeFromFile("maze.txt")
createMazeFromFile("maze2.txt")
open = PriorityQueue() #all the nodes that r looked at
open.put(Node.START_NODE)
closed = [] #currnt path list, more exlcuisve, so all the nodes that cause expansion

def Astar() -> bool:
    bestNode: Node = open.get(timeout=1)
    bestNode.color = CLOSED_NODE_COLOR if bestNode.type != Node.TYPE_START else STARTING_NODE_COLOR
    closed.append(bestNode)
    if bestNode is Node.END_NODE:
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
    
                
                


running: bool = True
winnerFound: bool = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BACKGROUND_COLOR)
    if not winnerFound:
        winnerFound = Astar()
    if winnerFound:
        print("Winner found")
    drawMaze()
    pygame.display.flip()
    time.sleep(0.1)
pygame.quit()
