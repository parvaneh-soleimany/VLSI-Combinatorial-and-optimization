import math
import time
from datetime import timedelta
from minizinc import Instance, Model, Solver
from utils import *
from tqdm import tqdm

instances = import_instances('../../instances/')

model = Model("cp_rot.mzn")
chuffed = Solver.lookup("chuffed")
start_time = time.time()
solve_end_time = 0
solved_numbers = 0
ins_number = []
ins_time = []
for i in tqdm(range(len(instances))):
    circuits, n, w, ordered_circuits, sorted_indexes = get_variables(instances, i)
    timeout = time.time() + 60*5
    instance = Instance(chuffed, model)
    instance['circuits'] = circuits
    instance['w'] = w
    instance['n'] = n
    instance['sorted_indexes'] = sorted_indexes
    solve_start_time = time.time()
    result = instance.solve(timeout=timedelta(minutes=5), processes=4, free_search = True)
    if time.time() >= timeout:
        print(f'Instance-{i+1} Fail: Timeout')
    else:
        ins_number.append(i+1)
        ins_time.append(time.time() - solve_start_time)
        solve_end_time += (time.time() - solve_start_time)
        solved_numbers += 1
        pos_x = result['pos_x']
        pos_y = result['pos_y']
        height = result['height']
        rot = result['rot']
        solution = output_solution(w, height,ordered_circuits, pos_x, pos_y,rot, f'../out/texts/out-{i+1}.txt')
        plot_solution(solution, f'../out/plots/out-{i+1}.png')
        print(f'Instance-{i+1} Solved!')
    

end_time = time.time() - start_time
print("time of execution: ", end_time)
print("mean time of execution: ", solve_end_time /solved_numbers)
print("solved instances: ", solved_numbers)

print("instances==",ins_number)
print("time(ms)==",ins_time)
