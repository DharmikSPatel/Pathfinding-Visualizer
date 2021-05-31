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
STARTING_NODE_COLOR = (217, 200, 119)
ENDING_NODE_COLOR = (217, 174, 137)
WHITE = "white"
font1: font.Font = font.SysFont("Arial", 15)



maze = []
startingNode = None



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
            maze[i].append(Node(i, j, color, type))

def drawMaze():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            draw.rect(screen, maze[i][j].color, maze[i][j].rect)
            imgFont = font1.render(f" {maze[i][j].getGCost()}+{maze[i][j].getHCost()}={str(maze[i][j].getFCost()) + maze[i][j].getArrow()}", True, WHITE)
            screen.blit(imgFont, maze[i][j].rect)
    
    start = 0
    end = len(maze[0])*Node.SIZE
    for i in range(len(maze)):
        draw.line(screen, WHITE, (Node.SIZE*i, start), (Node.SIZE*i, end))
    draw.line(screen, WHITE, (Node.SIZE*(i+1), start), (Node.SIZE*(i+1), end))

    start = 0
    end = len(maze)*Node.SIZE
    for i in range(len(maze[0])):
        draw.line(screen, WHITE, (start, Node.SIZE*i), (end, Node.SIZE*i))
    draw.line(screen, WHITE, (start, Node.SIZE*(i+1)), (end, Node.SIZE*(i+1)))
    

createMaze(0, 0, 10, 10, (2, 4), (9, 9))

open = PriorityQueue() #all the nodes that r looked at
open.put(Node.START_NODE)
closed = [] #currnt path list, more exlcuisve, so all the nodes that cause expansion

"""
for i in range(max(Node.START_NODE.x-1, 0), min(Node.START_NODE.x+2, len(maze))):
    for j in range(max(Node.START_NODE.y-1, 0), min(Node.START_NODE.y+2, len(maze[i]))):
        curNode: Node = maze[i][j]
        if curNode is Node.START_NODE:
            continue
        print((i, j))
        """
def Astar() -> bool:
    bestNode: Node = open.get(timeout=1)
    bestNode.color = "red"
    print(f"Best Node {bestNode}")
    if bestNode is Node.END_NODE:
        return True
    closed.append(bestNode)
    for i in range(max(bestNode.x-1, 0), min(bestNode.x+2, len(maze))):
        for j in range(max(bestNode.y-1, 0), min(bestNode.y+2, len(maze[i]))):
            curNode: Node = maze[i][j]
            if curNode is bestNode or curNode in closed:
                continue
            curNode.color = "blue"
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
    time.sleep(1)
pygame.quit()
