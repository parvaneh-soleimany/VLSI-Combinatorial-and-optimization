from pulp import *

def LP(min_height, max_height, n, w, x, y):
    
    #Define variables to solve
    height = LpVariable("height", lowBound=min_height, upBound=max_height, cat=LpInteger)
    pos_x = [LpVariable(f'pos_x{i}', lowBound=0, upBound=w-min(x), cat=LpInteger) for i in range(n)]
    pos_y = [LpVariable(f'pos_y{j}', lowBound=0, upBound=max_height-min(y), cat=LpInteger) for j in range(n)]
    delta = [[LpVariable(f"delta{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    x_ij = [[LpVariable(f"x{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    y_ij = [[LpVariable(f"y{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]

    
    #Define Problem
    lp_problem = LpProblem("LP_VLSI", LpMinimize)
    
    #The variable we want to minimize
    lp_problem += height
    
    
    #Add constraints to solver
    #....................................Boundaries Constraint..........................................
    
    for i in range(n):
        #constraint for checking that end points of each ciircuit do not exceed plate boundaries
        lp_problem += pos_x[i] + x[i] <= w
        lp_problem += pos_y[i] + y[i] <= height
    
    #.....................................constraint to prevent overlap.............................
    for i in range(n):
            for j in range(i+1, n):
                lp_problem += pos_x[i] + x[i] <= pos_x[j]  + w * (x_ij[i][j] + y_ij[i][j])
                lp_problem += pos_x[i] - x[j] >= pos_x[j]  - w * (1  - x_ij[i][j] + y_ij[i][j]) 
                lp_problem += pos_y[i] + y[i] <= pos_y[j]  + max_height * (1  + x_ij[i][j] - y_ij[i][j])
                lp_problem += pos_y[i] - y[j] >= pos_y[j]  - max_height * (2  - x_ij[i][j] - y_ij[i][j])
    #....................................symmetry breaking constraint for flip..........................
    lp_problem += pos_x[0]==0
    lp_problem += pos_y[0]==0
    
    #....................................Solve the problem..............................................
    switch_solver = True
    if switch_solver:
        #Free Student Version
        path_to_cplex = "/Applications/CPLEX_Studio221/cplex/bin/x86-64_osx/cplex"
        solver = CPLEX_CMD(path=path_to_cplex, msg=False, timeLimit=300, options=["set preprocessing symmetry 5"])
    else:
        #Requires Certificate
        solver = CPLEX_PY(msg=False, timeLimit=300)

    lp_problem.solve(solver)
    
    pos_x_sol = []
    pos_y_sol = []
    if lp_problem.status == 1:
        for i in range(n):
            pos_x_sol.append(round(pos_x[i].varValue))
            pos_y_sol.append(round(pos_y[i].varValue))
        h = round(height.varValue)
    else:
        try:
            l = round(lp_problem.solverModel.getVarByName("height").X)
            for i in range(n):
                pos_x_sol.append(round(lp_problem.solverModel.getVarByName(f"pos_x{i}").X))
                pos_y_sol.append(round(lp_problem.solverModel.getVarByName(f"pos_y{i}").X))
        except BaseException as err:
            print(err)
            return 'fail'
    
    solution = [h, pos_x_sol, pos_y_sol, lp_problem.solutionTime]

    return solution
