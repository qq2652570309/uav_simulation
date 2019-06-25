import numpy as np

class dataGenerator:
    def __init__(self, row=0, column=0):  
        self.row = row
        self.column = column
        self.dataSet = np.ndarray(shape=(self.row, self.column, self.row*self.column), dtype=np.float32)

    def genertating(self):
        for r in range(self.dataSet.shape[0]):
            for c in range(self.dataSet.shape[1]):
                self.dataSet[r][c] = np.arange(self.row*self.column)

    def getDataSet(self):
        return self.dataSet
            
