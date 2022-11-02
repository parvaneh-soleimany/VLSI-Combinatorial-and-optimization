from pulp import *

def LP(min_height, max_height, n, w, x, y):
    
    #Define variables to solve
    height = LpVariable("height", lowBound=min_height, upBound=max_height, cat=LpInteger)
    height.setInitialValue(min_height)
    pos_x = [LpVariable(f'pos_x{i}', lowBound=0, upBound=w-min(x[i],y[i]), cat=LpInteger) for i in range(n)]
    pos_y = [LpVariable(f'pos_y{j}', lowBound=0, upBound=max_height-min(x[j],y[j]), cat=LpInteger) for j in range(n)]
    delta = [[[LpVariable(f"delta{i + 1}{j + 1}{d + 1}", cat=LpBinary) for d in range(4)] for j in range(n)] for i in range(n)]
    rot = [LpVariable(f"rot{i + 1}", lowBound=0, upBound=1, cat=LpBinary) for i in range(n)]
    x_ij = [[LpVariable(f"x{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    y_ij = [[LpVariable(f"y{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    M = max(w,max_height)

    #Define Problem
    lp_problem = LpProblem("LP_VLSI", LpMinimize)
    
    #The variable we want to minimize
    lp_problem += height
    
    
    #Add constraints to solver
    #....................................Boundaries Constraint..........................................
    for i in range(n):
        #constraint which do not rotate the squares as well as circuits with height more than plate width
        if x[i] == y[i] or y[i] > w:
            lp_problem += rot[i] == 0
            
        #constraint for checking that end points of each circuit do not exceed plate boundaries    
        lp_problem += - pos_x[i] <= 0
        lp_problem += - pos_y[i] <= 0
        lp_problem += pos_x[i] + (x[i] * (1 - rot[i]) + y[i] * rot[i]) <= w
        lp_problem += pos_y[i] + (x[i] * rot[i] + y[i] * (1 - rot[i])) <= height
        
        #.....................................constraint to prevent overlap.............................        
        for i in range(n):
            for j in range(i+1, n):
                lp_problem += pos_x[i] + rot[i]*y[i] + (1-rot[i])*x[i] <= pos_x[j]  + M * (x_ij[i][j] + y_ij[i][j])
                lp_problem += pos_x[i] - rot[j]*y[j] - (1-rot[j])*x[j] >= pos_x[j]  - M * (1  - x_ij[i][j] + y_ij[i][j]) 
                lp_problem += pos_y[i] + rot[i]*x[i] + (1-rot[i])*y[i] <= pos_y[j]  + M * (1 + x_ij[i][j] - y_ij[i][j])
                lp_problem += pos_y[i] - rot[j]*x[j] - (1-rot[j])*y[j] >= pos_y[j]  - M * (2 - x_ij[i][j] - y_ij[i][j])    
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
    rot_sol = []
    if lp_problem.status == 1:
        for i in range(n):
            pos_x_sol.append(round(pos_x[i].varValue))
            pos_y_sol.append(round(pos_y[i].varValue))
            rot_sol.append(round(rot[i].varValue))     
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
    
    solution = [h, pos_x_sol, pos_y_sol, rot_sol, lp_problem.solutionTime]

    return solution







