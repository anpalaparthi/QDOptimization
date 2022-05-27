
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math
from datetime import datetime
from map_elites import  ToyDomainSolution, Solution, SolutionArchive

# def sphere - sphere objective function
# def rastrigin - 2nd objective function

# sphere objective function (currently being used as performance)
#   using formula sum(1->n) of x_i^2
def sphere(ndim_vector):
    sum = 0
    for num in np.nditer(ndim_vector):  
            sum += (num * num) 
    return sum

# rastrigin objective function
def rastrigin(ndim_vector):
    sum = 10 * len(ndim_vector)
    for num in np.nditer(ndim_vector):  
            # x^2 - 10cos(2pix)
            sum += (num * num) 
            sum -= 10 * math.cos(2 * math.pi * num)
    return sum

# input parameters for map-elites algorithm
num_dims = 20
# actual number of iterations for experiment - 2.5 million
# num_iterations = 2500000
num_iterations = 100000
num_initial = 100
mutation_power = 0.5
# solutions_map = {}
# performance_map = {}
archive_res = 512
solutions_archive = SolutionArchive(archive_res)


#call map-elites for ToyDomain experiment
print("Start time:")
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

ToyDomainSolution.find_map_elites(solutions_archive, num_iterations, num_initial, mutation_power, num_dims, sphere)
solutions_archive.generate_heatmap(-1)
print('all done')

print("End time:")
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
