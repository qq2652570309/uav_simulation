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
        self.trainingSets = []
        self.groundTruths = []

        self.startPoints = self.choosePoints(self.startPointsNum)
        self.endPoints = self.choosePoints(self.endPointsNum)


    def generate(self):
        startTime = time.time()
        for i in range(self.iteration):
            ge = Generator(self.row, self.column, self.time)
            trainingSet = ge.genertateTrainingSet()
            groundTruth = ge.genertateGroundTruth()
            self.trainingSets.append(trainingSet)
            self.groundTruths.append(groundTruth)
        self.trainingSets = np.array(self.trainingSets)
        self.groundTruths = np.array(self.groundTruths)
        fo = open("log.txt", "w")
        fo.write("total running time: {0}\n".format(time.time() - startTime))
        fo.write("training set shape: {0}\n".format(self.trainingSets.shape))
        fo.write("ground truth shape: {0}\n".format(self.groundTruths.shape))
        fo.close()
        print('total running time: {0}'.format(time.time() - startTime))
        print('training set shape: {0}'.format(self.trainingSets.shape))
        print('ground truth shape: {0}'.format(self.groundTruths.shape))


    def getData(self):
        return self.trainingSets, self.groundTruths
    
    def save(self):
        np.save('trainingSets', self.trainingSets)
        np.save('groundTruths', self.groundTruths)

    # maybe startPointsNum != endPointsNum
    def choosePoints(self, pointsNum):
        return np.random.choice(self.row*self.column, pointsNum, replace=False)