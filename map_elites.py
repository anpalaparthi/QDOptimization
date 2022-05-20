# class ToyDomainSolution (extends Solution abstract class if need to support dif types of solutions)
#   Attributes:
#   - n-dimensional array to store config of solution
#   - n = # of dimensions
#   - fitness = output of performance function
#   - performance() = function used to calculate fitness
#   
#   Functions:
#   - mutate(): return new ToyDomainSolution
#       -- use Gaussian noise to generate randomly new solution based on this one
#   - generate() - create random solution
#       -- randomly generate n numbers and store in n-dimensional array
#   - behavior() 
#       -- return the lower-dimension behavior description
#   - constructor(performance()) 
#       -- generate random solution, use given performance function for run()



# genHeatMap(solutions map, performance map)

from re import I
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

class Solution:
    def __init__(self):
        raise Exception("Solution child class needs to be defined")

    def __init__(self, numDims, perf):
        self.numDimensions = numDims
        self.performance = perf
        self.fitness = None
        #print("inside solution constructor")
        # child class should fill in fitness using given performance function

    def mutate(self):
        raise Exception("Solution child class mutate() needs to be defined")

    def generate(self):
        raise Exception("Solution child class generate() needs to be defined")

    def behavior(self):
        raise Exception("Solution child class behavior() needs to be defined")

class ToyDomainSolution(Solution):
    def __init__(self, numDims, perf):
        super().__init__(numDims, perf)
        self.vals = None
        self.generate()
        self.fitness = self.performance(self.vals)

        #print("inside toy domain constructor")

    def mutate(self):
        # use gaussian to create new solution based on this one
        noise = np.random.normal(loc=0, scale=0.5, size=self.numDimensions)

        mutatedSolution = ToyDomainSolution(self.numDimensions, self.performance)
        mutatedSolution.vals = (self.vals + noise)
        return mutatedSolution


    def generate(self):
        # fill in n-dimensional array with random values
        #   (choosing range of random values to be [-5.12, 5.12])
        #self.vals = 5.12 * np.random.random_sample(size = self.numDimensions) - 5.12
        self.vals = 10.24 * np.random.random_sample(size = self.numDimensions) - 5.12


    def behavior(self):
        # return lower dimension description of this solution

        lowerHalf = self.clip(self.vals[:self.numDimensions//2])
        upperHalf = self.clip(self.vals[self.numDimensions//2:])

        return np.sum(lowerHalf), np.sum(upperHalf)

    def clip(self, arr):
        # for num in arr:
        for num in np.nditer(arr):  
            if num < -5.12 or num > 5.12:
                num = 5.12 / num
        return arr


# void findMapElites(): run map-elites algorithm and update maps accordingly
# findMapElites(solutions map, performance map, # iterations,
#                   # initialElites, defaultSolution (to give perf, numdims, etc))
# for iter 1 -> I:
#     if iter < G:
#         x' = random_solution()
#     else :
#         x = random_selection(X)
#         x' = random_variation(x)

#     b' = feature_desc(x')
#     p' = perf(x')
    
#     if(P(b') = 0 or P(b') < p'):
#         P(b') = p'
#         X(b') = x'

def findMapElites(solsMap, perfMap, numIterations, numInitial, solType, solTemp):

    count = 0
    for i in range(numIterations):
        if (i < numInitial):
            newSol = solType(solTemp.numDimensions, solTemp.performance)
        else:
            randomDesc, randomSol = random.choice(list(solsMap.items()))
            newSol = randomSol.mutate()
        
        newBehavior = newSol.behavior()
        newPerformance = newSol.fitness
        #print("fitness = ", newSol.fitness)
        
        if newBehavior not in solsMap.keys() or perfMap[newBehavior] < newPerformance:
            perfMap[newBehavior] = newPerformance
            solsMap[newBehavior] = newSol
        
        if i % 1600 == 0:
            generateHeapMap(perfMap, count)
            count += 1
#             print("new")
#         else:
#             print("exists")

def generateHeapMap(performanceMap, count):
    perfs = list(performanceMap.values())

    behaviors = performanceMap.keys()
    behaviorACoord = [i[0] for i in behaviors]
    behaviorBCoord = [i[1] for i in behaviors]



    df = pd.DataFrame({'x': behaviorACoord, 'y' : behaviorBCoord, 'z' : perfs})

    sc = plt.scatter(df.x, df.y, 0.1, c=df.z, cmap='plasma_r')
    if count == 0:
        plt.colorbar(sc)
    filename = 'heatmap' + chr(count+65) + '.png'
    plt.savefig(filename)


    print(len(perfs))
    print(chr(count+65) +"done")