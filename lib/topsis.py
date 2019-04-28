import math

# step 1 - standardize the decision matrix
def _standardize(array):
    array[0] = [att * (-1) for att in array[0]] # rssi values
    for row in array:
        sum = 0
        for att in row:
            sum += pow(att, 2)
        sum = math.sqrt(sum)
        row[:] = [att / sum for att in row]
    return array

# step 2 - construct weighted standardized decision matrix
def _multiply_weights(array, w):
    for i in range(len(w)):
        for j in range(len(array[i])):
            array[i][j] *= w[i]
    return array

# step 3, 4, 5
def _solutions(array):

    # step 3 - determine ideal solution and negative ideal solution
    # up 0,2
    # down, 1,3
    # + ideal solution, max up, min down -> min, min, max, min
    # - ideal solution, min up, max down -> max, max, min, max
    pos = [min(array[0]), min(array[1]), max(array[2]), min(array[3])]
    neg = [max(array[0]), max(array[1]), min(array[2]), max(array[3])]
    print('I:', pos)
    print('AI:', neg)
    s_pos = []
    s_neg = []
    for j in range(len(array[0])):
        # step 4 - determine separation from ideal solution
        s_pos.append( math.sqrt(sum([ pow(array[i][j] - pos[i],2) for i in range(len(array)) ])) )
        # step 5 - determine separation from negative ideal solution
        s_neg.append( math.sqrt(sum([ pow(array[i][j] - neg[i],2) for i in range(len(array)) ])) )
    print('Ideal:', s_pos)
    print('Anti-Ideal:', s_neg)
    return (s_pos, s_neg)

def _det_ideal_sol(sol):
    s_pos = sol[0]
    s_neg = sol[1]
    sum = [s_pos[i] + s_neg[i] for i in range(len(s_pos))]
    closeness = [s_neg[i] / sum[i] for i in range(len(s_pos))]
    print('Closeness:', closeness)
    return closeness

def closeness(dec_matrix, weights):
    dec_matrix = _standardize(dec_matrix)
    dec_matrix = _multiply_weights(dec_matrix, weights)
    solutions = _solutions(dec_matrix)
    return _det_ideal_sol(solutions)
