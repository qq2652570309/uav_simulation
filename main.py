import numpy as np
import logging
from simulator import Simulator 

logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)

logging.info('Started')
# s = Simulator(iteration = 2, row=4, column=4, time=5, startPointsNum=3, endPointsNum=3)
s = Simulator(iteration = 20, row=16, column=16, time=60, startPointsNum=20, endPointsNum=20)
# s = Simulator(iteration = 100, row=64, column=64, time=60, startPointsNum=100, endPointsNum=100)
s.generate()
logging.info('Finished')
np.save('trainingSets.npy', s.trainingSets)
np.save('groundTruths.npy', s.groundTruths)
# logging.info('trainingSets: \n{0}'.format(s.trainingSets))
# logging.info('groundTruths: \n{0}'.format(s.groundTruths))
