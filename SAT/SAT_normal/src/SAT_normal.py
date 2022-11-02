from tqdm import tqdm
from utils import read_instances, plot_solution, output_solution, get_variables
from constraints import SAT
from z3 import *

instances = read_instances('../../instances/')
for instance_index in tqdm(range(len(instances))):
    n, x, y, w, min_height, max_height = get_variables(instances[instance_index])
    height = min_height
    find_result = False
    while not find_result and height <= max_height:
        solver = Solver()
        times = 300 * 1000
        solver.set(timeout=times)
        sol = SAT(solver, height, n, w, x, y)
        if (sol) :
            pos_x, flag, pos_y= [False]*(n), [False]*(n), [False]*(n)
            for i in range(len(sol)):
                for j in range(len(sol[0])):
                    for c in range(n):
                        if sol[i][j] == c and not(flag[c]):
                            flag[c] = True
                            pos_x[c] = i
                            pos_y[c] = j
            circuits = [[x[i], y[i], pos_x[i], pos_y[i]] for i in range(n)]
            solution = output_solution(w, height, circuits, pos_x, pos_y, f'../out/texts/out-{i+1}.txt')
            plot_solution(solution, f'../out/plots/out-{i+1}.png')
            print('finish')
        
            find_result = True
        height = height + 1
    if(not find_result):
        print("\nFailed to solve instance %i" % (instance_index + 1))
    


