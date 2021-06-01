from maze import Maze
from node import Node
from game import Game
from colors import *
from queue import PriorityQueue
import pygame as pygame
from pygame import font,display,time
from pygame_widgets import Button, Slider


pygame.init()
screenSize = (1000, 900)
screen = display.set_mode(screenSize)

game = Game("stop", 100)
maze = Maze(dimin={"row": 20, "col": 4, "start": (0, 0), "end": (19, 3)})
maze = Maze(fileName="maze.txt")

open = PriorityQueue() #all the nodes that r looked at
open.put(Node.START_NODE)
closed = [] #currnt path list, more exlcuisve, so all the nodes that cause expansion


def startStopButtonOnClick():
    startButton.text = game.startStopButtonOnClick()
startButton = Button(screen, 200, 700, 100, 40, text="Start", onClick=startStopButtonOnClick)
speedSlider = Slider(screen, 20, 700, 100, 20, min=1, max=100, step=1, initial=100)


def events() -> bool:
    stop = False
    gameEvents = pygame.event.get()
    for event in gameEvents:
        if event.type == pygame.QUIT:
            stop = True
    startButton.listen(gameEvents)
    speedSlider.listen(gameEvents)
    return not stop

def drawMenu():
    startButton.draw()
    speedSlider.draw()

def Astar() -> bool:
    if game.gameState == "stop":
        return False
    bestNode: Node = open.get(timeout=1)
    bestNode.color =CLOSED_NODE_COLOR if bestNode.type != Node.TYPE_START else STARTING_NODE_COLOR
    closed.append(bestNode)
    if bestNode is Node.END_NODE:
        for row in maze:
            for node in row:
                if node.type == Node.TYPE_EMPTY:
                    node.color = EMPTY_COLOR
        bestNode.highlightPath()
        return True
    for i in range(max(bestNode.y-1, 0), min(bestNode.y+2, len(maze))):
        for j in range(max(bestNode.x-1, 0), min(bestNode.x+2, len(maze[i]))):
            curNode: Node = maze[i][j]
            if curNode is bestNode or curNode in closed or curNode.type == Node.TYPE_WALL:
                continue
            curNode.color =OPEN_NODE_COLOR
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
    running = events()
    screen.fill(BACKGROUND_COLOR)
    game.setSpeed(speedSlider.getValue())
    if time.get_ticks() >= game.speedThreshold:
        if not winnerFound:
            winnerFound = Astar()
        if winnerFound:
            pass
        game.speedThreshold = time.get_ticks() + game.speed
    drawMenu()
    maze.draw(screen)
    pygame.display.flip()
pygame.quit()
