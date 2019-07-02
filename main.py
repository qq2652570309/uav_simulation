from simulator import Simulator 

# s = Simulator(iteration = 25, row=64, column=64, time=60, startPointsNum=10, endPointsNum=10)
# s.generate()
# s.save()

s = Simulator(iteration = 2, row=3, column=4, time=3, startPointsNum=10, endPointsNum=10)
s.generate()
print(s.trainingSets)