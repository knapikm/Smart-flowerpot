import math

# step 1 - standardize the decision matrix
def standardize(array):
    array[0] = [att * (-1) for att in array[0]] # rssi values
    for row in array:
        sum = 0
        for att in row:
            sum += pow(att, 2)
        sum = math.sqrt(sum)
        row[:] = [att / sum for att in row]
    return array

# step 2 - construct weighted standardized decision matrix
def multiply_weights(array, w):
    for i in range(len(w)):
        for j in range(len(array[i])):
            array[i][j] *= w[i]
    return array

# step 3, 4, 5
def solutions(array):

    # step 3 - determine ideal solution and negative ideal solution
    # up 0,2
    # down, 1,3
    # + ideal solution, max up, min down -> min, min, max, min
    # - ideal solution, min up, max down -> max, max, min, max
    pos = [max(array[0]), min(array[1]), max(array[2]), min(array[3])]
    neg = [min(array[0]), max(array[1]), min(array[2]), max(array[3])]

    s_pos = []
    s_neg = []
    for j in range(len(array[0])):
        # step 4 - determine separation from ideal solution
        s_pos.append( math.sqrt(sum([ pow(array[i][j] - pos[i],2) for i in range(len(array)) ])) )
        # step 5 - determine separation from negative ideal solution
        s_neg.append( math.sqrt(sum([ pow(array[i][j] - neg[i],2) for i in range(len(array)) ])) )
    return (s_pos, s_neg)

def det_ideal_sol(sol):
    s_pos = sol[0]
    s_neg = sol[1]
    sum = [s_pos[i] + s_neg[i] for i in range(len(s_pos))]
    ideal = [s_neg[i] / sum[i] for i in range(len(s_pos))]
    return ideal
