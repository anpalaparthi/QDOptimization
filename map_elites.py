# class ToyDomainSolution (extends Solution abstract class if need to support dif types of solutions)
#   Attributes:
#   - n-dimensional array to store config of solution
#   - n = # of dimensions
#   - fitness = output of performance function
#   - performance() = function used to calculate fitness
#   
#   Functions:
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

# abstract Solution class to define how any solution type should
#   be given to the map-elites algorithm
class Solution:
    
    def __init__(self):
        raise Exception("Solution child class needs to be defined")

    #save the number of dimensions of each solutions and the performance function to be used
    def __init__(self, numDims, perf):
        self.numDimensions = numDims
        self.performance = perf
        self.fitness = None
        # child class should fill in fitness using given performance function

    def mutate(self):
        raise Exception("Solution child class mutate() needs to be defined")

    def generate(self):
        raise Exception("Solution child class generate() needs to be defined")

    def behavior(self):
        raise Exception("Solution child class behavior() needs to be defined")

#Solution object to use
class ToyDomainSolution(Solution):

    #Constructor for ToyDomain object with given dimensions and performance function
    def __init__(self, numDims, perf):
        super().__init__(numDims, perf)
        self.vals = None

        # generate random values n random values for the n-dimensional object, and calculate fitness 
        self.generate()
        self.fitness = self.performance(self.vals)


    # use Gaussian noise to generate randomly new solution based on this one
    def mutate(self):
        noise = np.random.normal(loc=0, scale=0.5, size=self.numDimensions)

        mutatedSolution = ToyDomainSolution(self.numDimensions, self.performance)
        mutatedSolution.vals = (self.vals + noise)
        return mutatedSolution


    # fill in n-dimensional array with random values
    #   (choosing range of random values to be [-5.12, 5.12])
    def generate(self):
        self.vals = 10.24 * np.random.random_sample(size = self.numDimensions) - 5.12

    # return lower dimension description of this solution
    #   (sum of first n/2 components, sum of second n/2 components)
    def behavior(self):

        sumLower = 0
        sumUpper = 0
        for i in range(len(self.vals)):
            if i < (len(self.vals) / 2):
                sumLower += self.clipVal(self.vals[i])
            else:
                sumUpper += self.clipVal(self.vals[i])

        return sumLower, sumUpper

    # clip all the values in an array
    # def clip(self, arr):
    #     # for num in arr:
    #     for num in np.nditer(arr):  
    #         if num < -5.12 or num > 5.12:
    #             num = 5.12 / num
    #     return arr

    # clip function to restrict values to [-5.12, 5.12] range
    def clipVal(self, num):
        if num < -5.12 or num > 5.12:
                return 5.12 / num
        return num

# function to run map-elites algorithm
def findMapElites(solsMap, perfMap, numIterations, numInitial, solType, solTemp):

    #variable for printing heatmaps to file
    count = 0

    # generate numIterations number of solutions
    for i in range(numIterations):
        
        #initialize maps w/ numInitial random solutions
        if (i < numInitial):
            newSol = solType(solTemp.numDimensions, solTemp.performance)
        else:

            #for remaining solutions, generate new solution by mutating an existing solution 
            randomDesc, randomSol = random.choice(list(solsMap.items()))
            newSol = randomSol.mutate()
        
        # find the new behavior and fitness of the generated solution
        newBehavior = newSol.behavior()
        newPerformance = newSol.fitness

        #update the maps with this is a new/better solution
        oldPerf = perfMap.get(newBehavior)
        if oldPerf == None or oldPerf > newPerformance:
            
            perfMap[newBehavior] = newPerformance
            solsMap[newBehavior] = newSol
        
        # generate 25 heatmaps intermittently over the course of map-elites algorithm 
        if i % (numIterations // 5) == 0:
            generateHeapMap(perfMap, count)
            count += 1

# helper function to create and update heat & save to file
def generateHeapMap(performanceMap, count):
    
    # separate the performance map into three lists for x/y axis and z values (aka performance/heat)
    behaviorACoord = []
    behaviorBCoord = []
    perfs = []
    for k, v in performanceMap.items():
        perfs.append(v)
        behaviorACoord.append(k[0])
        behaviorBCoord.append(k[1])
        

    # format data into a pandas data frame
    df = pd.DataFrame({'x': behaviorACoord, 'y' : behaviorBCoord, 'z' : perfs})
    df = df.sort_values(by=['x'])
    
    # plot scatter plot with performances as color values
    sc = plt.scatter(df.x, df.y, 0.1, c=df.z, cmap='plasma_r')
    if count == 0:
        plt.colorbar(sc)

    #save heatmap to file (first will be labelled A, second B, etc)
    filename = 'heatmap' + chr(count+65) + '.png'
    plt.savefig(filename)

    #print current update to terminal (number of cells printed and which file generated)
    print(len(perfs))
    print(chr(count+65) +"done")





# Pseudocode for map-elites algorithm from paper
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