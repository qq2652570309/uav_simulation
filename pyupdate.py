import numpy as np

A = np.array([0,1,2,3])
B = np.array([0,1,2,3])



startRow = 0
startCol = 0
endRow = 3
endCol = 3

# t * r * c
G = np.zeros((8,4,4))

# r * c * t
# G = np.zeros((4,4,8))

r =  np.arange(startRow, endRow+1)
c = np.arange(startCol+1, endCol+1)
t1 = np.arange(0, len(r))
t2 = np.arange(t1[-1]+1, t1[-1] + len(c)+1)


G[t1,startRow, r] += 1
G[t2, c, endCol] += 1

# G[startRow, r, t1] += 1
# G[c, endCol, t2] += 1

print(G)
