import numpy as np

class Grid:

    def __init__(self, row=0, col=0, time=0):
        self.ROW = row
        self.COLUMN = col
        self.grid = np.zeros((self.ROW, self.COLUMN), dtype=np.int16)
        self.time = time
        self.currentTime = 0

    def getGrid(self):
        return self.grid

    
    def drawPath(self, startX, startY, endX, endY):
        # first row then column
        flyTime = (endY - startY) + (endX - startX) + 1
        
        if flyTime + self.currentTime < self.time:
            # uav is able to reach destination in specific time
            if endY > startY:
                self.grid[startX, startY:endY+1] += 1
            else:
                self.grid[startX, endY:startY+1] += 1

            if endX > startX:
                self.grid[startX+1:endX+1, endY] += 1
            else:
                self.grid[endX:startX, endY] += 1 
        else:
            # uav is not able to reach destination in specific time
            remainingTime = self.time - self.currentTime
            
            if remainingTime >= (endY - startY + 1):
                # enough time to finish row 
                self.grid[startX, startY:endY+1] += 1
                remainingTime = remainingTime - (endY - startY + 1)
            else:
                # not enough to finish row
                self.grid[startX, startY:startY+(remainingTime)] += 1
                remainingTime = 0

            if remainingTime > 0:
                # exist remaining time for column
                self.grid[startX+1:endX+1, endY] += 1

            pass


    def drawPath1(self, startX, startY, endX, endY):
        # first row then column
        if endY > startY:
            self.grid[startX, startY:endY+1] += 1
        else:
            self.grid[startX, endY:startY+1] += 1

        if endX > startX:
            self.grid[startX+1:endX+1, endY] += 1
        else:
            self.grid[endX:startX, endY] += 1 

        
    
    