from colors import *
from pygame import font
font.init()
class Game:
    minSpeed = 2000
    myFont = font.SysFont("Arial", 15)
    def __init__(self, gameState: str, startSpeed: int) -> None:
        self.gameState = gameState
        self.speed = Game.minSpeed - (Game.minSpeed * startSpeed / 100)
        self.speedThreshold = 0
    def startStopButtonOnClick(self) -> str:
        returnSurface = Game.myFont.render(self.gameState, True, TEXT_COLOR)
        if self.gameState == "start":
            self.gameState = "stop"
        elif self.gameState == "stop":
            self.gameState = "start"
        return returnSurface
    def setSpeed(self, newSpeed: int) -> None:
        self.speed = Game.minSpeed - (Game.minSpeed * newSpeed / 100)

