import logging
import numpy as np
from simulator import Simulator

logger = logging.getLogger()
logger.disabled = True

logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)

logging.info('Started')
# s = Simulator(iteration=2, row=4, column=4, time=5, startPointsNum=3, endPointsNum=3)
s = Simulator(iteration=1000, row=16, column=16, time=32, startPointsNum=30, endPointsNum=30)
# s = Simulator(iteration=100, row=64, column=64, time=60, startPointsNum=120, endPointsNum=120)
s.generate()
logging.info('Finished')
np.save('trainingSets.npy', s.trainingSets)
np.save('groundTruths.npy', s.groundTruths)
# logging.info('trainingSets: \n{0}'.format(s.trainingSets))
# logging.info('groundTruths: \n{0}'.format(s.groundTruths))
