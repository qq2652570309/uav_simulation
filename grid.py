import numpy as np

class Grid (object):

    def __init__(self, x, y, t):
       self.grid = np.zeros((x, y, t), dtype=np.int16)

    def getGrid(self):
        return self.grid

    