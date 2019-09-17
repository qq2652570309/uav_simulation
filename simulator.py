'''
# In channel, 0th is status that uav is launching at this second
# 1st is launching rate of this point
# 2nd and 3rd is (x, y) postion of destination point
'''
import time
import random
import logging
import numpy as np
from Area import Area

class Simulator:
    def __init__(self, batch = 1, time=60, row=0, column=0,  taskNum=10, timeInterval=5):
        self.batch = batch
        self.row = row
        self.column = column
        self.time = time
        self.taskNum = taskNum
        self.timeInterval = timeInterval
        self.area = Area(0.1,0.9)
        # In channel, 1st and 2nd are (x, y) launching location, 3rd and 4th are (x, y) destination location
        # self.trainingSets = np.zeros(shape=(self.iteration, self.time, self.row, self.column, 4), dtype=np.float32)
        self.trainingSets = np.zeros(shape=(self.batch, self.time, taskNum, 4), dtype=np.float32)
        self.groundTruths = np.zeros(shape=(self.batch, self.time, self.row, self.column), dtype=np.float32)
        # record all launching and landing postions
        # self.positions = np.zeros(shape=(self.batch,  self.row, self.column), dtype=np.float32)
        self.totalFlyingTime = 0
        self.totalUavNum = 0
        # logging.info('finish init\n')


    def generate(self):
        startTimeTotal = time.time()
        
        for batch_idx in range(self.batch):
            startTimeIter = time.time()

            self.area = Area(0.1, 0.9)
            # self.setColor(batch_idx, self.area.la, self.area.da)

            # time iteration
            for currentTime in range(self.time):
                
                # task iteration
                startPositions = self.area.getLaunchPoint(n=self.taskNum)
                for task_idx, task_val in zip(range(len(startPositions)), startPositions):
                    startRow, startCol, launchingRate = task_val
                    startRow = int(startRow)
                    startCol = int(startCol)
                    succ = np.random.uniform(0,1) <= launchingRate
                    
                    # if there is a launching UAV
                    if succ:
                        self.totalUavNum += 1
                        endRow, endCol = self.area.getDestination()
                        remainingTime = self.time - currentTime
                        
                        # add info into channel
                        self.trainingSets[batch_idx,currentTime,task_idx,0] = startRow
                        self.trainingSets[batch_idx,currentTime,task_idx,1] = startCol
                        self.trainingSets[batch_idx,currentTime,task_idx,2] = endRow
                        self.trainingSets[batch_idx,currentTime,task_idx,3] = endCol
                        
                        # logging.info('      At time {0}, ({1}, {2}) --> ({3}, {4})'.format(currentTime, startRow, startCol, endRow, endCol))
                        flyingTime = 0
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
                        self.groundTruths[batch_idx,t1,startRow,r] += 1
                        remainingTime -= len(r)
                        self.totalFlyingTime += len(r)

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
                            self.groundTruths[batch_idx,t2, c, endCol] += 1
                            self.totalFlyingTime += len(c)
            # logging.info('End {0} iteration, cost {1}\n'.format(batch_idx, time.time() - startTimeIter))
        # logging.info('finish generate, cost {0}'.format(time.time() - startTimeTotal))
        

    def setColor(self, batch_idx, startPositions, endPositions):
        for sp, ep in zip(startPositions, endPositions):
            self.positions[batch_idx, sp[0], sp[1]] = 0.2
            self.positions[batch_idx, ep[0], ep[1]] = 0.5


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.disabled = True

    logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)

    logging.info('Started')
    startTimeIter = time.time()
    s = Simulator(batch=1, row=32, column=32, time=100)
    s.generate()
    print('UAV Avg Flying Time: ', s.totalFlyingTime/s.totalUavNum)

    logging.info('Finished')
    np.save('data/raw_trainingSets.npy', s.trainingSets)
    np.save('data/raw_groundTruths.npy', s.groundTruths)
    # np.save('data/positions.npy', s.positions)
    print('Simulation Total Time: ', time.time() - startTimeIter)