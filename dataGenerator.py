import numpy as np
import random
from grid import Grid

class dataGenerator:
    def __init__(self, row=0, column=0, time=60):
        self.row = row
        self.column = column
        self.time = time
        self.launchingRates = np.ndarray(shape=(self.row, self.column), dtype=np.float32)
        self.destinationRates = np.ndarray(shape=(self.row, self.column, self.row*self.column), dtype=np.float32)
        self.trainingSet = np.ndarray(shape=(self.row, self.column, self.row*self.column), dtype=np.float32)
        self.groundTruth = Grid(self.row, self.column, self.time)

    def genertateTrainingSet(self):
        for r in range(self.row):
            for c in range(self.column):
                self.launchingRates[r][c] = random.uniform(0, 1)
                self.destinationRates[r][c] = np.random.dirichlet(np.ones(self.row * self.column),size=1).flatten()
                self.trainingSet[r][c] = self.launchingRates[r][c] * self.destinationRates[r][c]
        return self.trainingSet

    def genertateGroundTruth(self):
        for currentTime in range(self.time):
            for r in range(self.row):
                for c in range(self.column):
                    if self.isLaunch(self.launchingRates[r][c]):
                        endX, endY = self.destinationPosition(self.destinationRates[r][c])
                        self.groundTruth.drawPath(r,c,endX,endY,currentTime)
        return self.groundTruth.getGrid()


    # launching_rate is a float number
    def isLaunch(self, launching_rate):
        possibility = random.uniform(0,1)
        print(possibility)
        if (possibility >= launching_rate):
            return True
        else:
            return False

    # destRates is a 1 x N array containing all destination rates
    def destinationPosition(self, destination_rates):
        possibility = random.uniform(0,1)
        for i, val in enumerate(destination_rates):
            if (possibility <= val):
                row = i // self.column
                col = i % self.column
                return row, col
            else:
                possibility -= val
