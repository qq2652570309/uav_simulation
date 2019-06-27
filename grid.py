import numpy as np

class Grid:

    def __init__(self, row=0, col=0, time=0):
        self.ROW = row
        self.COLUMN = col
        self.grid = np.zeros((self.ROW, self.COLUMN), dtype=np.int16)
        self.time = time
        # print('grid size: ({0}, {1})  total time: {2} currentTime: {3}'.format(self.ROW, self.COLUMN, self.time, self.currentTime))

    def getGrid(self):
        # return self.grid / self.time
        return self.grid
    
    def drawPath(self, startX, startY, endX, endY, currentTime):
        
        # first row then column
        remainingTime = self.time - currentTime

        # print('before row, remainingTime: {0}'.format(remainingTime))
        if abs(endY - startY)+1 <= remainingTime:
            # enough time to finish row
            if endY > startY:
                self.grid[startX, startY:endY+1] += 1
            else:
                self.grid[startX, endY:startY+1] += 1
            remainingTime = remainingTime - abs(endY - startY)-1
        else:
            # not enough to finish row
            if endY > startY:
                self.grid[startX, startY:startY+remainingTime] += 1
            else:
                self.grid[startX, startY+1-remainingTime:startY+1] += 1
            remainingTime = 0

        # print('before row column, remainingTime: {0}'.format(remainingTime))
        if remainingTime > 0:
            if abs(endX - startX) <= remainingTime:
                # enough time to finish column
                if endX > startX:
                    self.grid[startX+1:endX+1, endY] += 1
                else:
                    self.grid[endX:startX, endY] += 1
            else:
                # not enough time to finish column
                if endX > startX:
                    self.grid[startX+1:startX+1+remainingTime, endY] += 1
                else:
                    self.grid[startX-remainingTime:startX, endY] += 1
                
        