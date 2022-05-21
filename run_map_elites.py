import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
from map_elites import  ToyDomainSolution, Solution, findMapElites, generateHeapMap

# def sphere - sphere objective function
# def rastrigin - 2nd objective function

# sphere objective function (currently being used as performance)
#   using formula sum(1->n) of x_i^2
def sphere(nDimVector):
    sum = 0
    for num in np.nditer(nDimVector):  
            sum += (num * num) 
    return sum

# rastrigin objective function
def rastrigin(nDimVector):
    sum = 10 * len(nDimVector)
    for num in np.nditer(nDimVector):  
            # x^2 - 10cos(2pix)
            sum += (num * num) 
            sum -= 10 * math.cos(2 * math.pi * num)
    return sum

# input parameters for map-elites algorithm
numDims = 20
# actual number of iterations for experiment - 2.5 million
# numIterations = 2500000
numIterations = 200000
numInitial = 10
solutionTemplate = ToyDomainSolution(numDims, sphere)
solutionsMap = {}
performanceMap = {}

#call map-elites for ToyDomain experiment
findMapElites(solutionsMap, performanceMap, numIterations, numInitial, ToyDomainSolution, solutionTemplate)
generateHeapMap(performanceMap, -1)
print('all done')
