from itertools import combinations
from z3 import *

def SAT(solver, height, n, w, x, y):
    plate = [[[Bool(f"plate_{i}_{j}_{c}") for c in range(n)] for j in range(height)] for i in range(w)]
    for i in range(w):
        for j in range(height):
            solver.add(at_most_one(plate[i][j]))
            solver.add(at_least_one(plate[i][j]))

    for c in range(n):
        positions = []
        for i in range(w - x[c] + 1):
            for j in range(height - y[c] + 1):
                positions.append(And([plate[i2][j2][c] for i2 in range(i, i + x[c]) for j2 in range(j, j + y[c])]))
        solver.add(at_least_one(positions))
    
    solver.add(biggest_rectangle(w, x, y, plate))
    
    sol = []
    if solver.check() == sat:
        m = solver.model()
        for i in range(w):
            sol.append([])
            for j in range(height):
                for c in range(n):
                    if m.evaluate(plate[i][j][c]):
                        sol[i].append(c)
    return sol

def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def biggest_rectangle(w, x, y, plate):
    return [And([plate[i][j][0] for i in range(x[0]) for j in range(y[0])])]
