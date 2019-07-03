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
        self.groundTruths = np.zeros(shape=(self.iteration, self.time, self.row, self.column), dtype=np.float32)


    def generate(self):
        startTime = time.time()
        for index in range(self.iteration):
            print('\n*----At {0} iteration----'.format(index))
            startPoints = self.choosePoints(self.startPointsNum)
            startPositions = list(map(lambda x: (x//self.column, x%self.column), startPoints))
            endPoints = self.choosePoints(self.endPointsNum)
            endPositions = list(map(lambda x: (x//self.column, x%self.column), endPoints))

            for startRow, startCol in startPositions:
                # print('--------At start Point ({0}, {1})--------'.format(startRow, startCol))
                # set traning sets
                self.trainingSets[index,:,startRow,startCol] = np.random.uniform(0, 1)
                # generate ground truth
                for currentTime in range(self.time):
                    # launchingRate = self.trainingSets[index,currentTime,startRow,startCol]
                    # currentRate = np.random.uniform(0,1)
                    # succ = currentRate <= launchingRate
                    # print('   At time {0}, lr={1}, cr={2}, succ={3}'.format(currentTime, launchingRate, currentRate, succ))
                    succ = np.random.uniform(0,1) <= self.trainingSets[index,currentTime,startRow,startCol]
                    if succ:
                        endRow, endCol  = random.choice(endPositions)
                        remainingTime = self.time - currentTime
                        # print('      from ({0}, {1}) --> ({2}, {3}), remainingTime={4}'.format(startRow, startCol, endRow, endCol, remainingTime))
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
                        self.groundTruths[index,t1,startRow,r] += 1
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
                            self.groundTruths[index,t2, c, endCol] += 1





    def draw(self, index, startPositions, endPositions):

        for startRow, startCol in startPositions:
            for currentTime in range(self.time):
                succ = np.random.uniform(0,1) <= self.trainingSets[index,currentTime,startRow,startCol]
                if succ:
                    endRow, endCol  = random.choice(endPositions)
                    remainingTime = self.time - currentTime

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
                    self.groundTruths[index,t1,startRow,r] += 1
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
                        self.groundTruths[index,t2, c, endCol] += 1

            
    def test(self):
        startRow = 0
        startCol = 0
        endRow = 2
        endCol = 3

        # t * r * c
        G = np.zeros((8,3,4))

        currentTime = 1
        totalTime = 8

        remainingTime = totalTime - currentTime

        if remainingTime >= abs(startCol-endCol)+1 :
            # enough time for horizontal
            r =  np.arange(startCol, endCol+1)
        else:
            # not enough time for horizontal
            r = np.arange(startCol, startCol+remainingTime)
        t1 = np.arange(currentTime, currentTime+len(r))
        G[t1,startRow, r] += 1
        remainingTime -= len(r)

        if remainingTime > 0 :
            # exists time for vertical
            if remainingTime >= abs(startRow-endRow) :
                # enough time for vertical
                c = np.arange(startRow+1, endRow+1)
            else:
                # not enough time for vertical
                c = np.arange(startRow+1, startRow+remainingTime+1)
            t2 = np.arange(t1[-1]+1, t1[-1] + len(c)+1)
            G[t2, c, endCol] += 1
            
        print(G)

    # maybe startPointsNum != endPointsNum
    def choosePoints(self, pointsNum):
        return np.random.choice(self.row*self.column, pointsNum, replace=False)

