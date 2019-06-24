# from grid import Grid
# from Node import Node
import numpy as np

class PathFinder:
    def __init__(self, startX=0, startY=0, endX=0, endY=0):
        self.ROW = 3
        self.COLUMN = 3
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        # self.startNode = Node(x=self.startX, y=self.startY)
        # self.targetNode = Node(x=self.endX, y=self.endY)
        self.grid = np.zeros((self.ROW, self.COLUMN), dtype=np.int16)


    def drawPath(self):
        if self.endX > self.startX:
            self.grid[self.startX:self.endX+1, self.endY] = 1
        else:
            self.grid[self.endX:self.startX+1, self.endY] = 1 

        if self.endY > self.startY:
            self.grid[self.startX, self.startY:self.endY+1] = 1
        else:
            self.grid[self.startX, self.endY:self.startY+1] = 1

    def getGrid(self):
        return self.grid

'''
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

    def save_grid(self):
        path = self.PathFinding()
        self.grid.fillGrid(path)
        np.save('result_grid', self.grid.getGrid())
'''    
