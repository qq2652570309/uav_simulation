import numpy as np

class Grid:

    def __init__(self, row=0, col=0, time=0):
        self.ROW = row
        self.COLUMN = col
        self.grid = np.zeros((self.ROW, self.COLUMN), dtype=np.int16)
        self.time = time
        self.currentTime = 54
        print('grid size: ({0}, {1})  total time: {2} currentTime: {3}'.format(self.ROW, self.COLUMN, self.time, self.currentTime))

    def getGrid(self):
        return self.grid

    
    def drawPath(self, startX, startY, endX, endY):
        # 先判断row是否能走完，row能走完用原方法走，走不完用remainTime走
        # 如果remainTime有剩余，判断是否column能走完，能走完用原方法走，走不完用remainTime走
        
        # first row then column
        flyTime = abs(endY - startY) + abs(endX - startX) + 1
        
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
            print('row remainingTime: {0}'.format(remainingTime))
            if remainingTime >= (endY - startY + 1):
                # enough time to finish row 
                self.grid[startX, startY:endY+1] += 1
                remainingTime = remainingTime - (endY - startY + 1)
            else:
                # not enough to finish row
                self.grid[startX, startY:startY+(remainingTime)] += 1
                remainingTime = 0
            print('column remainingTime: {0}'.format(remainingTime))
            print('endX={0} startX={1}'.format(endX, startX))
            # print('endX - startX = {0}'.format(endX - startX))
            if remainingTime > 0:
                # exist remaining time for column
                if remainingTime >= abs(endX - startX):
                    # eougth time to finish column
                    if (endX > startX):
                        # move down
                        self.grid[startX+1:endX+1, endY] += 1
                else:
                    # not enough time to finish column
                    if (endX > startX):
                        # move down
                        self.grid[startX+1:startX+(remainingTime+1), endY] += 1
                    else:   
                        # move up
                        self.grid[startX-(remainingTime):startX, endY] += 1



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

        
    
    