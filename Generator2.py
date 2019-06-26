import numpy as np
from grid import Grid

class Generator2:
    def __init__(self, width=0, height=0, num = 0):  
        self.height = height
        self.width = width
        self.num = num


from grid import Grid
from PathFinder import PathFinder
import numpy as np


height = 3
width = 4
num = 10

np.random.seed()

def getRand(height, width, num):
    x = np.random.randint(0, height, num)
    y = np.random.randint(0, width, num)
    return np.array([x,y]).transpose()


departures = getRand(height, width, num)
destinations = getRand(height, width, num)

grid = Grid(height, width)
result = []
for depart in departures:
    for dest in destinations:
        grid = Grid(height, width)
        grid.drawPath(depart[0], depart[1], dest[0], dest[1])
        result.append(grid.getGrid())

print(np.array(result)[0])
