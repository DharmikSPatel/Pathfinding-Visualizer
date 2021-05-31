from time import sleep
from pygame import Rect, math
from functools import total_ordering
import queue
import math


@total_ordering
class Node:
    TYPE_WALL = 0
    TYPE_EMPTY = 1
    TYPE_START = 2
    TYPE_END = 3
    START_NODE = None
    END_NODE = None
    SIZE = 90
    X_OFFSET = 0
    def __init__(self, x, y, color, type, g = 0, h = 0):
        self.x: int = x
        self.y: int = y
        self.color = color
        self.type: int = type
        if type == Node.TYPE_START:
            Node.START_NODE = self
        elif type == Node.TYPE_END:
            Node.END_NODE = self
        self.parrent: Node = None
    def setUpRect(self) -> Rect:
        self.rect: Rect = Rect(Node.SIZE*self.x+Node.X_OFFSET, Node.SIZE*self.y, Node.SIZE, Node.SIZE)
    def getArrow(self) -> str:
        if self.parrent == None:
            return ""
        if self.parrent.x == self.x-1 and self.parrent.y == self.y-1:
            return "←↑"
        if self.parrent.x == self.x and self.parrent.y == self.y-1:
            return "↑"
        if self.parrent.x == self.x+1 and self.parrent.y == self.y-1:
            return "→↑"
        if self.parrent.x == self.x+1 and self.parrent.y == self.y:
            return "→"
        if self.parrent.x == self.x+1 and self.parrent.y == self.y+1:
            return "→↓"
        if self.parrent.x == self.x and self.parrent.y == self.y+1:
            return "↓"
        if self.parrent.x == self.x-1 and self.parrent.y == self.y+1:
            return "←↓"
        if self.parrent.x == self.x-1 and self.parrent.y == self.y:
            return "←"
    def highlightPath(self, pathColor, startColor, endColor):
        if self.type != Node.TYPE_START and self.parrent != None:
            self.color = endColor if self.type == Node.TYPE_END else pathColor
            self.parrent.highlightPath(pathColor, startColor, endColor)
        elif self.type == Node.TYPE_START:
            self.color = startColor
        
        
        """
        if self.type == Node.END_NODE:
            self.color = endColor
            self.parrent.highlightPath(pathColor, startColor, endColor)
        elif self.type == Node.START_NODE:
            self.color = startColor
        else:
            self.color = pathColor
            self.parrent.highlightPath(pathColor, startColor, endColor)
        """
    def getGCost(self):
        if self.type != Node.TYPE_START and self.parrent != None:
            return self.parrent.getGCost() + int(math.sqrt((self.parrent.y - self.y)**2 + (self.parrent.x - self.x)**2)*10)
        return 0
    def getHCost(self):
        changeX: int = abs(Node.END_NODE.x - self.x)
        changeY: int = abs(Node.END_NODE.y - self.y)
        return int(math.sqrt((min(changeX, changeY))**2 + (min(changeX, changeY))**2)*10)+10*abs(changeY-changeX)
        '''
        directPath:int = int(math.sqrt((Node.END_NODE.y - self.y)**2 + (Node.END_NODE.x - self.x)**2)*10)
        if directPath%14 == 0:
            return directPath
        else:
            return directPath 
        '''
    def getFCost(self):
        return self.getGCost() + self.getHCost()

    def __eq__(self, other) -> bool:
        return False
        '''
        if other == None:
            return False
        return (self.getFCost(), self.getHCost(), self.getGCost()) == (other.getFCost(), other.getHCost(), other.getGCost())
        '''
    def __lt__(self, other) -> bool:
        if (self.getFCost(), self.getHCost()) == (other.getFCost(), other.getHCost()):
            return self.getGCost() > other.getGCost()
        else:
            return (self.getFCost(), self.getHCost()) < (other.getFCost(), other.getHCost())
    def __str__(self) -> str:
        return f"({self.getFCost()}, {self.getHCost()}, {self.getGCost()})\t ({self.x}, {self.y})"
    