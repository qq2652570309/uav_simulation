import numpy as np

class Grid:

    def __init__(self, row=0, col=0):
        self.ROW = row
        self.COLUMN = col
        self.grid = np.zeros((self.ROW, self.COLUMN), dtype=np.int16)

    def getGrid(self):
        return self.grid

    
    def drawPath(self, startX, startY, endX, endY):
        # first row then column
        if endY > startY:
            self.grid[startX, startY:endY+1] += 1
        else:
            self.grid[startX, endY:startY+1] += 1

        if endX > startX:
            self.grid[startX+1:endX+1, endY] += 1
        else:
            self.grid[endX:startX, endY] += 1 

        
    
    