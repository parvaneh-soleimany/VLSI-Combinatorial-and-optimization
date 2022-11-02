### Import the necessary libraries
from tqdm import tqdm

from utils import read_instances, plot_solution, output_solution, get_variables
from constraints import LP
from pulp import *

instances = read_instances('../../instances/')

start_time = time.time()
solve_end_time = 0
solved_numbers = 0

for i in tqdm(range(len(instances))):
    solve_start_time = time.time()
    n, x, y, w, min_height, max_height, sorted_indexes, ordered_circuits = get_variables(instances[i])
    sol = LP(min_height, max_height, n, w, x, y)
    
    if sol == 'fail':
        print("NO solution found")
    else:
        solve_end_time += (time.time() - solve_start_time)
        solved_numbers += 1
        circuits = [[x[k], y[k], sol[1][k], sol[2][k]] for k in range(n)]
        
        solution = output_solution(w, sol[0], circuits, sol[1], sol[2], f'../out/texts/out-{i+1}.txt')
        plot_solution(solution, f'../out/plots/out-{i+1}.png')
        print('finish')
    
end_time = time.time() - start_time
print("time of execution : ", end_time)
print("min time of execution : ", solve_end_time /solved_numbers)