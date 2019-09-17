import numpy as np
from simulator import Simulator
import logging
import time

class Preprocess:

    def __init__(self, groundTruth=None, trainingSets=None):
        if groundTruth is None:
            print("ground truth is none")
        else:
            self.gtr = groundTruth
        if trainingSets is None:
            print("training set is none")
        else:
            self.tsr = trainingSets
        
        logging.info('---Initial Shape---')
        print('---Initial Shape---')
        print('raw trainingSets', self.tsr.shape)
        print('raw groundTruth: ', self.gtr.shape)

    # save data from start to end
    def splitByTime(self, start=0, end=0):
        if end == 0:
            self.gtr = self.gtr[:, start:]
            self.tsr = self.tsr[:, start:]
        else:
            self.gtr = self.gtr[:, start:end]
            self.tsr = self.tsr[:, start:end]
        logging.info(self.tsr.shape)
        logging.info(self.gtr.shape)
        logging.info('splitByTime complete\n')


    # switch all elements to zero or one 
    def oneOrZero(self, gtr):
        m = np.median(gtr[gtr!=0])
        logging.info('median: {0}'.format(m))
        # self.gtr[self.gtr<=m] = 0
        # self.gtr[self.gtr>m] = 1
        gtr[gtr<m] = 0
        gtr[gtr>=m] = 1
        logging.info('oneOrZero complete\n')
        return gtr


    # ground truth only save the last second (the 30th second)
    def lastSecond(self):
        gtr1 = self.gtr[:,29:,:,:].reshape((1, 16, 16))
        print('self.gtr[:,29:,:,:]: ', self.gtr[:,29:,:,:].shape)
        print('gtr1: ', gtr1.shape)
        print('self.gtr == gtr1:', np.all(gtr1==self.gtr[:,29]))
        self.gtr = gtr1
        print('lastSecond complete\n')

    # print number of non-zeros and zeros
    def computeWeights(self, gtr):
        one = gtr[gtr>0].size
        zero = gtr[gtr==0].size
        logging.info('zero: {0}'.format(zero))
        logging.info('one: {0}'.format(one))
        logging.info('weight: {0}'.format(zero/one))
        logging.info('computeWeights complete\n')

    # nomalize groud truth as the last second
    def batchNormalize(self, gtr):
        for i in range(len(gtr)):
            gtr[i] = (gtr[i] - np.min(gtr[i])) / (np.max(gtr[i]) - np.min(gtr[i]))
        logging.info('min: {0}'.format(np.min(gtr)))
        logging.info('max: {0}'.format(np.max(gtr)))
        logging.info('mean: {0}'.format(np.mean(gtr)))
        logging.info('median: {0}'.format(np.median(gtr)))
        logging.info('batchNormalize complete\n')
        return gtr

    # broadcast one sample to many 
    def broadCast(self):
        self.tsr = np.broadcast_to(self.tsr, (10000, 30, 32, 32, 4))
        self.gtr = np.broadcast_to(self.gtr, (10000, 30, 32, 32))
        print(self.tsr.shape)
        print(self.gtr.shape)
        print('broadCast complete\n')
        
    # (30, 32, 32) --> (32, 32)
    def generateDensity(self, gtr):
        temp = np.sum(gtr, axis=1)
        logging.info(gtr.shape)
        logging.info('generateDensity complete\n')
        return temp

    def save(self, data, name='feature'):
        if name is 'feature':
            print('training_data_trajectory shape is {0}'.format(data.shape))
            np.save('data/training_data_trajectory.npy', data)
        elif name is 'cnn':
            print('training_label_density shape is {0}'.format(name))
            np.save('data/training_label_density.npy', data)
        else:
            print('training_label_trajectory.npy shape is {0}'.format(name))
            np.save('data/training_label_trajectory.npy', data)
        print('{0} save complete\n'.format(name))

    def checkGroundTruthIdentical(self, gtr):
        p = np.random.randint(0, len(gtr), 5)
        for i in range(1,5):
            logging.info(np.all(gtr[p[i]] == gtr[p[i-1]]))
        logging.info('check complete\n')
    
    def checkDataIdentical(self, data1, data2):
        # p = np.random.randint(0, len(data1), 5)
        for i in range(0,5):
            logging.info(np.all(data1[i] == data2[i]))
        logging.info('check complete\n')

    def averageLaunchingNumber(self):
        sum1 = np.sum(self.tsr[:,:, 0:4, 0:4, 0])
        sum2 = np.sum(self.tsr[:,:, 22:26, 23:26, 0])
        sum3 = np.sum(self.tsr[:,:, 27:31, 27:31, 0])
        sampleNum = self.tsr.shape[0]
        timeTotal = self.tsr.shape[1]
        ave1 = sum1 / sampleNum / timeTotal * 5
        ave2 = sum2 / sampleNum / timeTotal * 5
        ave3 = sum3 / sampleNum / timeTotal * 5
        print('In area1, average number of UAV launched: ', ave1)
        print('In area2, average number of UAV launched: ', ave2)
        print('In area3, average number of UAV launched: ', ave3)
        print('average lauching complete\n')


    def featureLabel(self):
        logging.info('generating lstm feature\n')
        self.save(self.tsr, 'feature')

        logging.info('generating lstm labels\n')
        lstmGt = np.copy(self.gtr)
        lstmGt = self.oneOrZero(lstmGt)
        self.computeWeights(lstmGt)
        self.save(lstmGt, 'lstm')

        logging.info('generating cnn labels\n')
        cnnGt = np.copy(self.gtr)
        cnnGt = self.oneOrZero(cnnGt)
        cnnGt = self.generateDensity(cnnGt)
        cnnGt = self.batchNormalize(cnnGt)
        self.computeWeights(cnnGt)
        self.save(cnnGt, 'cnn')
        logging.info('finish saving')

        self.checkDataIdentical(lstmGt, cnnGt)
        print('finish saving')



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.disabled = False
    logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('Started')

    s = Simulator(batch=10, row=32, column=32, time=90)
    startTimeTotal = time.time()
    s.generate()
    
    print('avg flying time: ', s.totalFlyingTime/s.totalUavNum)

    logging.info('Finished')
    print('avg flying time: ', s.totalFlyingTime/s.totalUavNum)
    # logging.info('finish generate, cost {0} \n'.format(time.time() - startTimeTotal))
    logging.info('avg flying time: {0} \n'.format( s.totalFlyingTime/s.totalUavNum))
    
    p = Preprocess(trainingSets=s.trainingSets, groundTruth=s.groundTruths)
    p.splitByTime(30)
    p.featureLabel()

    logging.info('Finished dataPreprocess')
    print('Finished dataPreprocess')
