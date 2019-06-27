import numpy as np
import time
from generator import Generator

class Simulator:
    def __init__(self, iteration = 1, row=0, column=0, time=60):
        self.iteration = iteration
        self.row = row
        self.column = column
        self.time = time
        self.trainingSets = []
        self.groundTruths = []
    

    def generate(self):
        startTime = time.time()
        for i in range(self.iteration):
            ge = Generator(self.row, self.column, self.time)
            trainingSet = ge.genertateTrainingSet()
            groundTruth = ge.genertateGroundTruth()
            self.trainingSets.append(trainingSet)
            self.groundTruths.append(groundTruth)
        fo = open("log.txt", "w")
        fo.write("total running time: {0}\n".format(time.time() - startTime))
        fo.write("training set shape: {0}\n".format(self.trainingSets[0].shape))
        fo.write("ground truth shape: {0}\n".format(self.groundTruths[0].shape))
        fo.close()
        print('total running time: {0}'.format(time.time() - startTime))
        print('training set shape: {0}'.format(self.trainingSets[0].shape))
        print('ground truth shape: {0}'.format(self.groundTruths[0].shape))


    def getData(self):
        return self.trainingSets, self.groundTruths
    
    def save(self):
        np.save('trainingSets', np.array(self.trainingSets))
        np.save('groundTruths', np.array(self.groundTruths))