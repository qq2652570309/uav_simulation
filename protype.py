import numpy as np
from grid import Grid


# create a matrix, sum of its elements is 1 
row = 5
col = 4

s = np.random.dirichlet(np.ones(col),size=row)

############################################################

row = 3
column = 3

test = Grid(x=row, y=column)
test.drawPath(startX=0, startY=2, endX=0, endY=2)
# print(test.getGrid())

arr = np.arange(row*column)
np.random.shuffle(arr)

for n in arr:
    print("{0} in array is: ({1}, {2})".format(n, n//row, n%column))
