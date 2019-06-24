from grid import Grid
from Node import Node

class PathFinder:
    def __init__(self, startX=0, startY=0, startT=0, endX=0, endY=0, endT=0):
        self.ROW = 30
        self.COLUMN = 30
        self.TIME = 60
        self.startX = startX
        self.startY = startY
        self.startT = startT
        self.endX = endX
        self.endY = endY
        self.endT = endT
        self.startNode = Node(x=self.startX, y=self.startY, t=self.startT)
        self.targetNode = Node(x=self.endX, y=self.endY, t=self.endT)
        self.grid = grid(x=self.ROW, y=self.COLUMN, t=self.TIME)

    def PathFinding(self):
        return None
        
