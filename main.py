from pygame import draw
from node import Node
import pygame
from pygame import Rect

pygame.init()
screen = pygame.display.set_mode([900, 900])
BACKGROUND_COLOR = (37, 59, 89)
STARTING_NODE_COLOR = (217, 200, 119)
ENDING_NODE_COLOR = (217, 174, 137)
WHITE = "white"




maze = []
def createMaze(x, y, r, c, start, end):  
    for i in range(r):
        maze.append([])
        for j in range(c):
            color = BACKGROUND_COLOR
            if (i, j) == start:
                color = STARTING_NODE_COLOR
            elif (i, j) == end:
                color = ENDING_NODE_COLOR
            maze[i].append(Node(Node.SIZE*i, Node.SIZE*j, color, Node.EMPTY))
def drawMaze():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            draw.rect(screen, maze[i][j].color, maze[i][j].rect)
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


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BACKGROUND_COLOR)
    drawMaze()
    pygame.display.flip()
pygame.quit()
