from generator import Generator

generator = Generator(3, 3, 5)

trainingSet = generator.genertateTrainingSet()
groundTruth = generator.genertateGroundTruth()


for time in range(len(generator.launchingPoints)):
    for i in range(len(generator.launchingPoints[time])):
        print('---------------')
        print('At {0} second, startPoint {1}, endPoint {2}'.format(\
            time,\
            generator.launchingPoints[time][i],\
            generator.destinationPoints[time][i]))
        print(generator.gridStatus[time][i])
        print('---------------')

