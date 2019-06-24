import numpy as np
from grid import Grid

row = 3
column = 3

test = Grid(x=row, y=column)
test.drawPath(startX=0, startY=2, endX=0, endY=2)
# print(test.getGrid())

arr = np.arange(row*column)
np.random.shuffle(arr)

for n in arr:
    print("{0} in array is: ({1}, {2})".format(n, n//row, n%column))
