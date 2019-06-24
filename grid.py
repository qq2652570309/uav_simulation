import numpy as np

class Grid:

    def __init__(self, x=0, y=0):
       self.grid = np.zeros((x, y), dtype=np.int16)

    def getGrid(self):
        return self.grid

    def drawPath(self, startX, startY, endX, endY):
        if endX > startX:
            self.grid[startX:endX+1, endY] = 1
        else:
            self.grid[endX:startX+1, endY] = 1 

        if endY > startY:
            self.grid[startX, startY:endY+1] = 1
        else:
            self.grid[startX, endY:startY+1] = 1
    
    