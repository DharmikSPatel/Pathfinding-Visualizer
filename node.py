from pygame import Rect


class Node:
    WALL = 0
    EMPTY = 1
    SIZE = 30
    def __init__(self, x, y, color, type):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.rect = Rect(x, y, Node.SIZE, Node.SIZE)
    