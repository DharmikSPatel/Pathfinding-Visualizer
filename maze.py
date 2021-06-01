from typing import Dict
from pygame import Surface, draw
from node import Node
from colors import *
screenSize = (1000, 900)
class Maze(list):


    def __init__(self, fileName: str = None, dimin: Dict = None) -> None:
        super().__init__()
        if fileName is not None:
            self.row, self.col = self._openWithFile(fileName)
        else:
            self.row, self.col = self._openWithDimins(dimin)
        
        Node.SIZE = int((screenSize[1] if max(self.row, self.col) == self.row else screenSize[0])/max(self.row, self.col))
        Node.X_OFFSET = int((1000-(Node.SIZE*self.col))/2)
        for row in self:
            for node in row:
                node.setUpRect() 
    def _openWithFile(self, fileName: str) -> tuple:
        with open(fileName, "r") as mazeFile:
            maxRow: int = 0
            maxCol: int = 0
            for line in mazeFile:
                self.append([])
                maxCol = len(line)
                for x in range(maxCol):
                    letter: str = line[x]
                    if letter == "*":
                        self[maxRow].append(Node(x, maxRow, EMPTY_COLOR, Node.TYPE_EMPTY))
                    elif letter == "w":
                        self[maxRow].append(Node(x, maxRow,WALL_COLOR, Node.TYPE_WALL))
                    elif letter == "s":
                        self[maxRow].append(Node(x, maxRow,STARTING_NODE_COLOR, Node.TYPE_START))
                    elif letter == "e":
                        self[maxRow].append(Node(x, maxRow,ENDING_NODE_COLOR, Node.TYPE_END))
                maxRow+=1
        return (maxRow, maxCol)
    def _openWithDimins(self, dimin: Dict) -> tuple:
        c = dimin["col"]
        r = dimin["row"]
        start = dimin["start"]
        end = dimin["end"]
        for i in range(r):
            self.append([])
            for j in range(c):
                color =EMPTY_COLOR
                type = Node.TYPE_EMPTY
                if (i, j) == start:
                    color =STARTING_NODE_COLOR
                    type = Node.TYPE_START
                elif (i, j) == end:
                    color =ENDING_NODE_COLOR
                    type = Node.TYPE_END
                self[i].append(Node(j, i, color, type))
        return (r, c)
    def draw(self, screen: Surface):
        for i in range(len(self)):
            for j in range(len(self[i])):
                draw.rect(screen, self[i][j].color, self[i][j].rect)
                #imgFont = font1.render(f" {maze[i][j].getGCost()}+{maze[i][j].getHCost()}={str(maze[i][j].getFCost()) + maze[i][j].getArrow()}", True, WHITE)
                #screen.blit(imgFont, maze[i][j].rect)
        
        start = 0
        end = len(self)*Node.SIZE
        for i in range(len(self[0])+1):
            draw.line(screen,LINE_COLOR, (Node.SIZE*i+Node.X_OFFSET, start), (Node.SIZE*i+Node.X_OFFSET, end))
        
        start = Node.X_OFFSET
        end = len(self[0])*Node.SIZE+Node.X_OFFSET
        for i in range(len(self)+1):
            draw.line(screen,LINE_COLOR, (start, Node.SIZE*i), (end, Node.SIZE*i))  

    