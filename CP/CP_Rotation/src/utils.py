import os
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def import_instances(folder):

    # Method to sort a list alphanumerically
    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key=alphanum_key)
        
    instances = []
    files = sorted_alphanumeric(os.listdir(folder))
    for file in files:
        with open(folder + file) as f:
            content = f.readlines()
            content = [x.strip() for x in content] 
            instances.append(content)
    return instances


def get_variables(instances, number):
    w = int(instances[number][0])
    n = int(instances[number][1])
    ordered_circuits = []
    circuits = []
    for value in instances[number][2:]:
        width, height = value.split(' ')
        circuits.append([int(width), int(height)])
    temp_sorted_indexes = [] 
    temp = [circuits[i][0]*circuits[i][1] for i in range(len(circuits))]
    arg_temp = np.array(temp)
    sorted_indexes = np.flip(np.argsort(arg_temp, order=None))
    for i in sorted_indexes:
        ordered_circuits.append(circuits[i])
        temp_sorted_indexes.append(i+1)
    sorted_indexes = temp_sorted_indexes
    return circuits, n, w, ordered_circuits, sorted_indexes


def output_solution(w, height,ordered_circuits, pos_x, pos_y, rot, file):
    solution = []
    solution.append(str(w) + ' ' + str(height))
    solution.append(len(ordered_circuits))
    
    for i in range(len(ordered_circuits)):
        if rot[i] == 0:
            solution.append(str(ordered_circuits[i][0]) + ' ' + str(ordered_circuits[i][1]) + ' ' + str(pos_x[i]) + ' ' + str(pos_y[i]))
        else:
            solution.append(str(ordered_circuits[i][1]) + ' ' + str(ordered_circuits[i][0]) + ' ' + str(pos_x[i]) + ' ' + str(pos_y[i]))
    with open(file, 'w') as output:
        for item in solution:
            output.write(str(item))
            output.write('\n')
    return solution

def plot_solution(solution, file=None):
    SIZE = 10
    fig, ax = plt.subplots()
    w = int(solution[0].split(' ')[0])
    height = int(solution[0].split(' ')[1])
    n = int(solution[1])
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    fig.set_size_inches(SIZE/(r-l), SIZE * height / w)
    legnd = []
    cmap = plt.cm.get_cmap('tab20', n)
    bound = np.linspace(0, 1, n + 1)
    for i in range(len(solution)-2):
        element = solution[i+2].split(' ')
        ax.broken_barh([(int(element[2]), int(element[0]))], (int(element[3]), int(element[1])), 
                        facecolors=[cmap(b) for b in bound[:-1]][i],
                        edgecolors=("white"), 
                        linewidths=(2,),)
        legnd.append("size: " + str(element[0]) + ", " + str(element[1]) +
                    "\nX: " + str(element[2]) + ",Y: " + str(element[3]))
        
    ax.set_xticks(range(w))
    ax.set_yticks(range(height + 1))
    ax.grid(color='w', linewidth = 1)
    ax.set_xlabel('Width')
    ax.set_ylabel('Height')
    bound_prep = np.round(bound * (n - 1), 2)
    plt.legend([mpatches.Patch(color=cmap(b)) for b in bound[:-1]],
               ['{}'.format(legnd[i], bound_prep[i + 1] - 0.01) for i in range(n)], bbox_to_anchor=(1 , 1),
               loc="upper left")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(file)
    plt.close()