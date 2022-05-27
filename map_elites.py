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
import seaborn as sns

# abstract Solution class to define how any solution type should
#   be given to the map-elites algorithm
class Solution:
    
    def __init__(self):
        raise Exception("Solution child class needs to be defined")

    #save the number of dimensions of each solutions and the performance function to be used
    def __init__(self, num_dims, perf):
        self.num_dimensions = num_dims
        self.performance = perf
        self.fitness = None
        # child class should fill in fitness using given performance function

    def mutate(self, sigma):
        raise Exception("Solution child class mutate() needs to be defined")

    def generate(self):
        raise Exception("Solution child class generate() needs to be defined")

    def behavior(self):
        raise Exception("Solution child class behavior() needs to be defined")

    @classmethod
    def find_map_elites(self, sols_map, perf_map, num_iters, num_initial, mutation_power):
        raise Exception("Solution child class find_map_elites() needs to be defined")
       

    
#Solution object to use
class ToyDomainSolution(Solution):

    #Constructor for ToyDomain object with given dimensions and performance function
    def __init__(self, num_dims, perf):
        super().__init__(num_dims, perf)
        self.vals = None

        # generate random values n random values for the n-dimensional object, and calculate fitness 
        self.generate()
        self.fitness = self.performance(self.vals)


    # use Gaussian noise to generate randomly new solution based on this one
    def mutate(self, sigma):
        noise = np.random.normal(loc=0, scale=sigma, size=self.num_dimensions)

        mutated_solution = ToyDomainSolution(self.num_dimensions, self.performance)
        mutated_solution.vals = (self.vals + noise)
        return mutated_solution


    # fill in n-dimensional array with random values
    #   (choosing range of random values to be [-5.12, 5.12])
    def generate(self):
        self.vals = np.random.uniform(low = -5.12, high = 5.12, size = self.num_dimensions)

    # return lower dimension description of this solution
    #   (sum of first n/2 components, sum of second n/2 components)
    def behavior(self):

        sum_lower = 0
        sum_upper = 0
        for i in range(len(self.vals)):
            if i < (len(self.vals) / 2):
                sum_lower += self.clip_val(self.vals[i])
            else:
                sum_upper += self.clip_val(self.vals[i])

        return sum_lower, sum_upper

    # clip all the values in an array
    # def clip(self, arr):
    #     # for num in arr:
    #     for num in np.nditer(arr):  
    #         if num < -5.12 or num > 5.12:
    #             num = 5.12 / num
    #     return arr

    # clip function to restrict values to [-5.12, 5.12] range
    def clip_val(self, num):
        if num < -5.12 or num > 5.12:
                return 5.12 / num
        return num
    
    # function to run map-elites algorithm
    @classmethod
    def find_map_elites(self, sols_archive, num_iters, num_initial, mutation_power, num_dimensions, performance):

        #variable for printing heatmaps to file
        count = 0

        # generate num_iters number of solutions
        for i in range(num_iters):
            
            #initialize maps w/ num_initial random solutions
            if (i < num_initial):
                new_sol = ToyDomainSolution(num_dimensions, performance)
            else:

                #for remaining solutions, generate new solution by mutating an existing solution 
                #random_desc, random_sol = random.choice(list(sols_map.items()))
                random_sol = sols_archive.random_solution()
                new_sol = random_sol.mutate(mutation_power)
            
            sols_archive.add_solution(new_sol)
            
            # generate 25 heatmaps intermittently over the course of map-elites algorithm 
            if i % (num_iters // 5) == 0:
                #self.generate_heatmap(perf_map, count)
                sols_archive.generate_heatmap(count)
                count += 1

    

class SolutionArchive:

    # attributes:
    #   -solutions map
    #   -performance map

    # functions:
    #   - addSolution()
    #   - randomSolution()
    #   - generateHeatmap()
    #   - findIndex() --> get index (a tuple of 2 floats) of which cell this index lies in 

    # more possible functions
    #   - removeSolution()
    #   - findSolution() --> return None if DNE

    # initialize empty dicts for solutions map (map behavior->solution)
    #   and for performance map (map behavior->performance)
    def __init__(self, res):
        self.sols_map = {}
        self.perf_map = {}
        self.archive_res = res
        
        max = 250
        min = -250
        # using max/min values as -250 to 250 static values
        print("res = ", self.archive_res)
        self.interval = (max-min) / self.archive_res
        print("interval = ", self.interval)
    
    def add_solution(self, solution):
        # find the new behavior and fitness of the generated solution
        #sol_behavior = solution.behavior()
        sol_idx = self.findIndex(solution)
        sol_performance = solution.fitness
        
        #update the maps with this is a new/better solution
        old_perf = self.perf_map.get(sol_idx)
        if old_perf == None or old_perf > sol_performance:
            
            self.perf_map[sol_idx] = sol_performance
            self.sols_map[sol_idx] = solution
        
    def findIndex(self, solution):
        #using max/min values as -250 to 250 static values
        sol_behaviorA, sol_behaviorB = solution.behavior()
        sol_behaviorA = sol_behaviorA // self.interval
        sol_behaviorB = sol_behaviorB // self.interval
        
        return sol_behaviorA * self.interval, sol_behaviorB * self.interval
    
    def random_solution(self):
        random_desc, random_sol = random.choice(list(self.sols_map.items()))
        return random_sol
    
    # helper function to create and update heat & save to file
    def generate_heatmap(self, count):
        
        # separate the performance map into three lists for x/y axis and z values (aka performance/heat)
        behaviorA_coord = []
        behaviorB_coord = []
        perfs = []
        for k, v in self.perf_map.items():
            perfs.append(v)
            behaviorA_coord.append(k[0])
            behaviorB_coord.append(k[1])
        
        # format data into a pandas data frame
        df = pd.DataFrame({'x': behaviorA_coord, 'y' : behaviorB_coord, 'z' : perfs})
        df = df.sort_values(by=['x'])
        df = df.pivot(index = 'x', columns = 'y', values='z')
        
#         # plot scatter plot with performances as color values
#         sc = plt.scatter(df.x, df.y, 1.5, c=df.z, cmap='plasma_r')
        showbar = False
        if count == 0:
            showbar = True

        ax = sns.heatmap(df, cbar = showbar, cmap='plasma_r')
    
        #save heatmap to file (first will be labelled A, second B, etc)
        filename = 'heatmap' + chr(count+65) + '.png'
        plt.savefig(filename)

        #print current update to terminal (number of cells printed and which file generated)
        print(len(perfs))
        print(chr(count+65) +"done")






# Pseudocode for map-elites algorithm from paper
# void find_map_elites(): run map-elites algorithm and update maps accordingly
# find_map_elites(solutions map, performance map, # iterations,
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