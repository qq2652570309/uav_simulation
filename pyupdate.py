import numpy as np


startRow = 0
startCol = 0
endRow = 2
endCol = 3

# t * r * c
G = np.zeros((8,3,4))

# r * c * t
# G = np.zeros((4,4,8))

'''
r =  np.arange(startCol, endCol+1)
c = np.arange(startRow+1, endRow+1)

t1 = np.arange(0, len(r))
t2 = np.arange(t1[-1]+1, t1[-1] + len(c)+1)


G[t1,startRow, r] += 1
G[t2, c, endCol] += 1

# G[startRow, r, t1] += 1
# G[c, endCol, t2] += 1

# print(G)
'''


startRow = 3
startCol = 2
endRow = 0
endCol = 0

# t * r * c
G = np.zeros((8,4,3))

currentTime = 5
totalTime = 8

remainingTime = totalTime - currentTime

if remainingTime >= abs(startCol-endCol)+1 :
    # enough time for horizontal
    if startCol < endCol :
        r =  np.arange(startCol, endCol+1)
    else:
        r = np.arange(endCol, startCol+1)[::-1]       
else:
    # not enough time for horizontal
    if startCol < endCol:
        r = np.arange(startCol, startCol+remainingTime)
    else:
        r = np.arange(startCol-remainingTime+1, startCol+1)[::-1]
t1 = np.arange(currentTime, currentTime+len(r))
G[t1,startRow, r] += 1
remainingTime -= len(r)

if remainingTime > 0 :
    # exists time for vertical
    if remainingTime >= abs(startRow-endRow) :
        # enough time for vertical
        if startRow < endRow:
            c = np.arange(startRow+1, endRow+1)
        else:
            c = np.arange(endRow, startRow)[::-1]
    else:
        # not enough time for vertical
        if startRow < endRow:
            c = np.arange(startRow+1, startRow+remainingTime+1)
        else:
            c = np.arange(startRow-remainingTime, startRow)[::-1]
    t2 = np.arange(t1[-1]+1, t1[-1] + len(c)+1)
    G[t2, c, endCol] += 1
    
print(G)


'''

import random

row=3
column=4
startPointsNum = 10

# out = np.random.choice(row*column, startPointsNum, replace=False)
# out = np.random.uniform(0,1,10)

input = np.array([3, 5, 6, 10])
out = list(map(lambda x: (x//column, x%column), input))
print(out)

# out = np.empty(shape=(1,1))
# out.append(1)
# out.append(2)
# out.append(3)
# print(out)    
'''

