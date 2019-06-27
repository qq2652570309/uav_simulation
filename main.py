from simulator import Simulator 

# s = Simulator(iteration = 20, row=64, column=64, time=60)
s = Simulator(iteration = 25, row=64, column=64, time=60)
s.generate()    
s.save()

