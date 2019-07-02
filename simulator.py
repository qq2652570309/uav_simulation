import numpy as np
import time
import random
from generator import Generator

class Simulator:
    def __init__(self, iteration = 1, row=0, column=0, time=60, startPointsNum=10, endPointsNum=10):
        self.iteration = iteration
        self.row = row
        self.column = column
        self.time = time
        self.startPointsNum = startPointsNum
        self.endPointsNum = endPointsNum
        self.trainingSets = np.zeros(shape=(self.iteration, self.time, self.row, self.column), dtype=np.float32)
        self.groundTruths = []


    def generate(self):
        startTime = time.time()
        for i in range(self.iteration):
            startPoints = self.choosePoints(self.startPointsNum)
            startPositions = list(map(lambda x: (x//self.column, x%self.column), startPoints))
            endPoints = self.choosePoints(self.endPointsNum)
            endPositions = list(map(lambda x: (x//self.column, x%self.column), endPoints))
            # grid = np.zeros(shape=(self.time, self.row, self.column), dtype=np.float32)

            for r, c in startPositions:
                # grid[:,r,c] = np.random.uniform(0, 1)
                self.trainingSets[i,:,r,c] = np.random.uniform(0, 1)
            # print(grid)
            

            

        #     ge = Generator(self.row, self.column, self.time)
        #     ts = ge.genertateTrainingSet()
        #     gt = ge.genertateGroundTruth()
        #     self.trainingSets.append(ts)
        #     self.groundTruths.append(gt)
        # self.trainingSets = np.array(self.trainingSets)
        # self.groundTruths = np.array(self.groundTruths)
        # fo = open("log.txt", "w")
        # fo.write("total running time: {0}\n".format(time.time() - startTime))
        # fo.write("training set shape: {0}\n".format(self.trainingSets.shape))
        # fo.write("ground truth shape: {0}\n".format(self.groundTruths.shape))
        # fo.close()
        # print('total running time: {0}'.format(time.time() - startTime))
        # print('training set shape: {0}'.format(self.trainingSets.shape))
        # print('ground truth shape: {0}'.format(self.groundTruths.shape))


    def getData(self):
        return self.trainingSets, self.groundTruths
    
    def save(self):
        np.save('trainingSets', self.trainingSets)
        np.save('groundTruths', self.groundTruths)

    # maybe startPointsNum != endPointsNum
    def choosePoints(self, pointsNum):
        return np.random.choice(self.row*self.column, pointsNum, replace=False)

