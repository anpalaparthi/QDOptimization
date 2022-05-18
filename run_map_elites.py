import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
from map_elites import  ToyDomainSolution, Solution, findMapElites

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
numIterations = 250
numInitial = 10
solutionTemplate = ToyDomainSolution(numDims, sphere)
solutionsMap = {}
performanceMap = {}

findMapElites(solutionsMap, performanceMap, numIterations, numInitial, ToyDomainSolution, solutionTemplate)
perfs = list(performanceMap.values())
#print("perfs:")
#print(perfs)

behaviors = performanceMap.keys()
#print("Behaviors")
#print(behaviors)
behaviorACoord = [i[0] for i in behaviors]
behaviorBCoord = [i[1] for i in behaviors]

#print("a coords")
#print(behaviorACoord)
#print("b coords")
#print(behaviorBCoord)


#numpyArray = np.array((behaviorACoord, behaviorBCoord, perfs), dtype=object)
#resultArray = np.transpose(numpyArray)

arrOfData = [behaviorACoord, behaviorBCoord, perfs]
resultArray = np.array([np.array(xi) for xi in arrOfData]).transpose()


#print("result array")
#print(resultArray)
#print ("perfs size = ", len(perfs))
#print ("a size = ", len(behaviorACoord))
#print ("b size = ", len(behaviorBCoord))

sns.heatmap(resultArray)
plt.show()

print("done")

