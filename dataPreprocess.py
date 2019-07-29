import numpy as np


class Preprocess:

    def __init__(self):
        self.gtr = np.load("data/groundTruths_raw.npy")
        self.tsr = np.load("data/trainingSets_raw.npy")
        print('raw trainingSets', self.tsr.shape)
        print('raw groundTruth: ', self.gtr.shape)

    def split(self):
        dgtr = self.gtr[:,-1:]
        print(dgtr.shape)
        print(np.sum(self.tsr[:,-1]))
        np.save('groundTruths_density.npy', dgtr)
        self.gtr = self.gtr[:,:-1]
        self.tsr = self.tsr[:,:-1]
        print('\nafter split')
        print('raw trainingSets', self.tsr.shape)
        print('raw groundTruth: ', self.gtr.shape)

    # only save the first sample after 30 seconds
    def from30toEnd(self):
        # self.gtr = self.gtr[:1, 30:]
        # self.tsr = self.tsr[:1, 30:]
        self.gtr = self.gtr[:, 30:]
        self.tsr = self.tsr[:, 30:]
        print(self.tsr.shape)
        print(self.gtr.shape)

    # switch all elements to zero or one 
    def oneOrZero(self):
        m = np.median(self.gtr[self.gtr!=0])
        print('median:',m)
        # self.gtr[self.gtr<=m] = 0
        # self.gtr[self.gtr>m] = 1
        self.gtr[self.gtr<m] = 0
        self.gtr[self.gtr>=m] = 1


    # ground truth only save the last second (the 30th second)
    def lastSecond(self):
        gtr1 = self.gtr[:,29:,:,:].reshape((1, 16, 16))
        print('self.gtr[:,29:,:,:]: ', self.gtr[:,29:,:,:].shape)
        print('gtr1: ', gtr1.shape)
        print('self.gtr == gtr1:', np.all(gtr1==self.gtr[:,29]))
        self.gtr = gtr1

    # print number of non-zeros and zeros
    def computeWeights(self):
        one = self.gtr[self.gtr>0].size
        zero = self.gtr[self.gtr==0].size
        print('zero:',zero)
        print('one:',one)
        print('weight:',zero/one)


    # nomalize groud truth as the last second
    def batchNomalize(self):
        self.gtr = (self.gtr - np.min(self.gtr)) / (np.max(self.gtr) - np.min(self.gtr))
        print('min: ', np.min(self.gtr))
        print('max: ', np.max(self.gtr))
        print('mean: ', np.mean(self.gtr))
        print('median: ', np.median(self.gtr))

    # broadcast one sample to many 
    def broadCast(self):
        self.tsr = np.broadcast_to(self.tsr, (10000, 30, 16, 16, 4))
        self.gtr = np.broadcast_to(self.gtr, (10000, 30, 16, 16))
        print(self.tsr.shape)
        print(self.gtr.shape)

    def saveData(self):
        np.save('data/trainingSets_diff.npy', self.tsr)
        np.save('data/groundTruths_diff.npy', self.gtr)

    def checkGroundTruthIdentical(self):
        a1 = self.gtr[0]
        a2 = self.gtr[10]
        a3 = self.gtr[100]
        a4 = self.gtr[1000]

        print(np.all(a1==a2))
        print(np.all(a1==a3))
        print(np.all(a1==a4))
        print(np.all(a3==a2))

p = Preprocess()
p.split()
p.from30toEnd()
p.oneOrZero()
p.computeWeights()
# p.broadCast()
p.checkGroundTruthIdentical()
p.saveData()