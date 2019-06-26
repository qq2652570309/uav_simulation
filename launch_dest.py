from grid import Grid
import numpy as np
import random


# launching_rate is a float number
def isLaunch(launching_rate):
    possibility = random.uniform(0,1)
    print(possibility)
    if (possibility >= launching_rate):
        return True
    else:
        return False

# destRates is a 1 x N array containing all destination rates
# rowLen is how many elements place in one row
def destinationPos(destination_rates, rowLen):
    possibility = random.uniform(0,1)
    for i, val in enumerate(destination_rates):
        if (possibility <= val):
            row = i // rowLen
            col = i % rowLen
            return row, col
        else:
            possibility -= val

# launching_rate = 0.5
# for x in range(10):
#     print(isLaunch(launching_rate))
# destRates = [1,1,1,1,1,1,1,1,1]
# r, c = destinationPos(destRates, 3)
# print(r, c)
