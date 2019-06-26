import numpy as np
from dataGenerator import dataGenerator

dg = dataGenerator(2, 2)

dg.genertating()
result =  dg.getDataSet()

print(result.shape)
print(result[0][0])
print(np.sum(result[0][0]))


# print(result[0][0] + result[0][1])

s = np.sum(result, axis = 2)
print(s)