import numpy as np


gtr = np.load("data/groundTruths_raw.npy")
tsr = np.load("data/trainingSets_raw.npy")
print(tsr.shape)
print(gtr.shape)

gtr = gtr[:1, 30:]
tsr = tsr[:1, 30:]
print(tsr.shape)
print(gtr.shape)

gtr29 = gtr[:,:-1]
print('path size: ', gtr29.shape)
gtrLast = gtr[:, -1:]
print('density size: ', gtrLast.shape)


m = np.median(gtr29[gtr29!=0])
print('median:',m)
gtr29[gtr29<m] = 0
gtr29[gtr29>=m] = 1


# 29 * 16 * 16 = 7424
# 5782 + 1642  = 7424
one = gtr29[gtr29>0].size
zero = gtr29[gtr29==0].size
print('zero:',zero)
print('one:',one)
print('weight:',zero/one)

# Normalize groud truth at the last second
gtr[0, -1] = (gtrLast - np.min(gtrLast)) / np.max(gtrLast) - np.min(gtrLast)
print('gtrLast min: ', np.min(gtrLast))
print('gtrLast max: ', np.max(gtrLast))
print('gtrLast mean: ', np.mean(gtrLast))
print('gtrLast median: ', np.median(gtrLast))


# the 0-28th timesteps are in range 0-1 and the last one is density 
'''
print(gtr[0, 27])
print()
print(gtr[0, 28])
print()
print(gtr[0, 29])
'''


tsr = np.broadcast_to(tsr, (10000, 30, 16, 16, 4))
gtr = np.broadcast_to(gtr, (10000, 30, 16, 16))
print(tsr.shape)
print(gtr.shape)


np.save('data/trainingSets_overfit.npy', tsr)
np.save('data/groundTruths_overfit.npy', gtr)


a1 = gtr[0]
a2 = gtr[10]
a3 = gtr[100]
a4 = gtr[1000]

print(np.all(a1==a2))
print(np.all(a1==a3))
print(np.all(a1==a4))
print(np.all(a3==a2))
