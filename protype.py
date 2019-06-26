import numpy as np
from grid import Grid


# create a matrix, sum of its elements is 1 
row = 2
col = 4

s = np.random.dirichlet(np.ones(row * col),size=1).flatten()
print(s)
launching_rate = 2
res = launching_rate * s
print(res)
