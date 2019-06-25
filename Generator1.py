import numpy as np
from grid import Grid

class Generator1:
    def __init__(self, width=0, height=0):  
        self.row = height
        self.column = width


    def randomPath(self, seed=None):
        np.random.seed(seed)
        result = []
        gridInfo = []
        departures = np.arange(self.row*self.column)
        np.random.shuffle(departures)

        for i in range(len(departures)):
            departure = departures[i]
            startX = departure//self.row
            startY = departure%self.column

            destinations = np.arange(self.row*self.column)
            np.random.shuffle(destinations)
            for destination in destinations:
                endX = destination//self.row
                endY = destination%self.column
                grid = Grid(x=self.row, y=self.column)
                grid.drawPath(startX=startX, startY=startY, endX=endX, endY=endY)
                result.append(grid.getGrid())
                
                info = {
                    'startX': startX,
                    'startY': startY,
                    'endX': endX,
                    'endY': endY,
                }
                gridInfo.append(str(info))
        return np.array(result), gridInfo


# print(result[1])
# print(gridInfo[1])
