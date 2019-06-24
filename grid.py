import numpy as np

class Grid:

    def __init__(self, x=0, y=0, t=0):
       self.grid = np.zeros((x, y, t), dtype=np.int16)

    def getGrid(self):
        return self.grid

    