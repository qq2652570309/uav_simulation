import numpy as np
import logging
from simulator import Simulator 


logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)

logging.info('Started')
s = Simulator(iteration = 2, row=4, column=4, time=5, startPointsNum=3, endPointsNum=3)
s.generate()
logging.info('Finished')
logging.info('trainingSets: \n{0}'.format(s.trainingSets))
logging.info('groundTruths: \n{0}'.format(s.groundTruths))
