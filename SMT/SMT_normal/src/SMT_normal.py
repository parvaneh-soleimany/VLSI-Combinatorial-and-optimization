### Import the necessary libraries
from tqdm import tqdm
from utils import read_instances, plot_solution, output_solution, get_variables
from constraints import SMT
from z3 import *

instances = read_instances('../../instances/')

for i in tqdm(range(len(instances))):
    n, x, y, w, min_height, max_height, sorted_indexes, ordered_circuits = get_variables(instances[i])
    sol = SMT(min_height, max_height, n, w, x, y)
    
    if sol == 'fail':
        print("NO solution found")
    else:
        circuits = [[x[k], y[k], sol[1][k], sol[2][k]] for k in range(n)]
        solution = output_solution(w, sol[0], circuits, sol[1], sol[2], f'../out/texts/out-{i+1}.txt')
        plot_solution(solution, f'../out/plots/out-{i+1}.png')
        print('finish')