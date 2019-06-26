import numpy as np
import random

class dataGenerator:
    def __init__(self, row=0, column=0):  
        self.row = row
        self.column = column
        self.dataSet = np.ndarray(shape=(self.row, self.column, self.row*self.column), dtype=np.float32)

    def genertating(self):
        for r in range(self.dataSet.shape[0]):
            for c in range(self.dataSet.shape[1]):
                launching_rate = random.uniform(0, 1)
                destination_rate = np.random.dirichlet(np.ones(self.row * self.column),size=1).flatten()
                self.dataSet[r][c] = launching_rate * destination_rate

    def getDataSet(self):
        return self.dataSet

