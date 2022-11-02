from z3 import *
import time

def SMT(min_height, max_height, n, w, x, y):
    
    #Define variables to solve
    height = Int("height")
    pos_x = [Int(f"pos_x_{i}") for i in range(n)]
    pos_y = [Int(f"pos_y_{i}") for i in range(n)]
    
    circuits_x = [Int(f"x_{i}") for i in range(n)]
    circuits_y = [Int(f"y_{i}") for i in range(n)]
    
    #Define Solver
    Solver = Optimize()
    Solver.set(timeout=300000)
    
    #assign x and y to the arrays acceptable by the solver
    Solver.add([And(circuits_x[i] == x[i], circuits_y[i] == y[i]) for i in range(n)])
    
    #Add constraints to solver
    
    #....................................Boundaries Constraint..........................................
    Solver.add([And(pos_x[i] >= 0, 
                    pos_y[i] >= 0,
                    pos_x[i] <= w - min(x),
                    pos_y[i] <= height - min(y)) for i in range(n)])
    
    #constraint for checking that end points of each circuit do not exceed plate boundaries
    Solver.add([And(pos_x[i] + circuits_x[i] <= w,
                    pos_y[i] + circuits_y[i] <= height) for i in range(n)])
    
    Solver.add(And(height <= max_height, height >= min_height))
    
    #.....................................constraint for preventing overlap.............................
    Solver.add([Or(pos_x[i] + circuits_x[i] <= pos_x[j],
                   pos_x[i] - circuits_x[j] >= pos_x[j],
                   pos_y[i] + circuits_y[i] <= pos_y[j],
                   pos_y[i] - circuits_y[j] >= pos_y[j]) for i in range(n-1) for j in range(i+1, n)])
    
    #....................................cumulative constraint..........................................
    Solver.add(cumulative(pos_y, circuits_y, circuits_x, w))
    Solver.add(cumulative(pos_x, circuits_x, circuits_y, height))
    
    #....................................symmetry breaking constraint for flip..........................
    Solver.add(And(pos_x[0] == 0, pos_y[0] == 0))
    
    #....................................Solve the problem..............................................
    Solver.minimize(height)
    start = time.time()
    if str(Solver.check()) == 'sat':
        model = Solver.model()
        sol_height= int(model[height].as_string())
        sol_pos_x = [int(model.evaluate(pos_x[i]).as_string()) for i in range(n)]
        sol_pos_y = [int(model.evaluate(pos_y[i]).as_string()) for i in range(n)]
        exec_time = time.time() - start
        sol = [sol_height, sol_pos_x, sol_pos_y, exec_time]
    else:
        sol = 'fail'
    
    return sol


def cumulative(S, D, R, C):
    schedule = []
    for resource in R:
        schedule.append(sum([If(And(S[i] <= resource, resource < S[i] + D[i]), R[i], 0) for i in range(len(S))]) <= C)
    return schedule


