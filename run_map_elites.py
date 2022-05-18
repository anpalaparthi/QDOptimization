import numpy as np
import math
from map_elites import  ToyDomainSolution, Solution, findMapElites

# def sphere - sphere objective function
# def rastrigin - 2nd objective function

def sphere(nDimVector):
    sum = 0
    for num in np.nditer(nDimVector):  
            sum += (nDimVector * nDimVector) 
    return sum

def rastrigin(nDimVector):
    sum = 10 * len(nDimVector)
    for num in np.nditer(nDimVector):  
            # x^2 - 10cos(2pix)
            sum += (nDimVector * nDimVector) 
            sum -= 10 * math.cos(2 * math.pi * num)
    return sum

numDims = 20
numIterations = 2500000
numInitial = 10
solutionTemplate = ToyDomainSolution(numDims, sphere)
solutionsMap = {}
performanceMap = {}

findMapElites(solutionsMap, performanceMap, numIterations, numInitial, ToyDomainSolution, solutionTemplate)


print("done")

