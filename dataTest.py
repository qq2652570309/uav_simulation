from generator import Generator

generator = Generator(3, 3, 5)

trainingSet = generator.genertateTrainingSet()
groundTruth = generator.genertateGroundTruth()

# print(trainingSet.shape)
# print(groundTruth)

# print(generator.launchingPoints)
for k, v in generator.launchingPoints.items():
    print('{0}: {1}'.format(k,v))

for k, v in generator.destinationPoints.items():
    print('{0}: {1}'.format(k,v))

