from generator import Generator
import time

class Simulator:
    def __init__(self, iteration = 1, row=0, column=0, time=60):
        self.iteration = iteration
        self.row = row
        self.column = column
        self.time = time
        self.result = {}
    

    def generate(self):
        startTime = time.time()
        for i in range(self.iteration):
            ge = Generator(self.row, self.column, self.time)
            trainingSet = ge.genertateTrainingSet()
            groundTruth = ge.genertateGroundTruth()
            self.result[i] = [trainingSet, groundTruth]
        print('total running time: ', time.time() - startTime)
        print('training set shape: ', self.result[0][0].shape)
        print('ground truth shape: ', self.result[0][1].shape)



    def getData(self):
        return self.result