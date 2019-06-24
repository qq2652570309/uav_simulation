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
        self.startNode = Node(x=self.startX, y=self.startY, time=self.startT)
        self.targetNode = Node(x=self.endX, y=self.endY, time=self.endT)
        self.grid = Grid(x=self.ROW, y=self.COLUMN, t=self.TIME)

    def PathFinding(self):
        foundPath = []
        curNode = self.startNode
        foundPath.append(curNode)

        # row movement
        while (True):
            if curNode.x == self.targetNode.x:
                # in same row
                break
            elif curNode.x < self.targetNode.x:
                curNode = Node(curNode.x + 1, curNode.y, curNode.t + 1)
            else:
                curNode = Node(curNode.x - 1, curNode.y, curNode.t + 1)
            foundPath.append(curNode)
        
        # col movement
        while (True):
            foundPath.append(curNode)
            if curNode.equals(self.targetNode):
                break
            elif curNode.y < self.targetNode.y:
                curNode = Node(curNode.x, curNode.y + 1, curNode.t + 1)
            else:
                curNode = Node(curNode.x, curNode.y - 1, curNode.t + 1)

        return foundPath


        
