import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
from map_elites import  ToyDomainSolution, Solution, findMapElites, generateHeapMap

# def sphere - sphere objective function
# def rastrigin - 2nd objective function

def sphere(nDimVector):
    sum = 0
    for num in np.nditer(nDimVector):  
            sum += (num * num) 
    #print("sphere sum = ", sum)
    return sum

def rastrigin(nDimVector):
    sum = 10 * len(nDimVector)
    for num in np.nditer(nDimVector):  
            # x^2 - 10cos(2pix)
            sum += (num * num) 
            sum -= 10 * math.cos(2 * math.pi * num)
    return sum

numDims = 20
# numIterations = 2500000
numIterations = 40000
numInitial = 10
solutionTemplate = ToyDomainSolution(numDims, sphere)
solutionsMap = {}
performanceMap = {}

findMapElites(solutionsMap, performanceMap, numIterations, numInitial, ToyDomainSolution, solutionTemplate)
generateHeapMap(performanceMap, -1)
print('all done')
