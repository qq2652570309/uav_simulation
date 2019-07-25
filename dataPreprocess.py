import numpy as np





gtr = np.load("data/groundTruths_raw.npy")
tsr = np.load("data/trainingSets_raw.npy")
print(tsr.shape)
print(gtr.shape)

gtr = gtr[:1, 30:]
tsr = tsr[:1, 30:]
print(tsr.shape)
print(gtr.shape)

m= np.median(gtr[gtr!=0])
print('median:',m)
# gtr[gtr<=m] = 0
# gtr[gtr>m] = 1
gtr[gtr<m] = 0
gtr[gtr>=m] = 1

one = gtr[gtr>0].size
zero = gtr[gtr==0].size
print('zero:',zero)
print('one:',one)
print('weight:',zero/one)


tsr = np.broadcast_to(tsr, (10000, 30, 16, 16, 4))
gtr = np.broadcast_to(gtr, (10000, 30, 16, 16))
print(tsr.shape)
print(gtr.shape)


# np.save('data/trainingSets_overfit.npy', tsr)
# np.save('data/groundTruths_overfit.npy', gtr)
# np.save('data/trainingSets_overfit_one.npy', tsr)
# np.save('data/groundTruths_overfit_one.npy', gtr)


a1 = gtr[0]
a2 = gtr[10]
a3 = gtr[100]
a4 = gtr[1000]

print(np.all(a1==a2))
print(np.all(a1==a3))
print(np.all(a1==a4))
print(np.all(a3==a2))

