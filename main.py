import random
import numpy as np
import copy
from grid import basic_state, basic_state2, tradeoff_state, complex_state, complex_one_path, complex_one_path_good_test, state_score, q_table


def createOccuranceGrid(stategrid):

    rows = len(stategrid)
    cols = len(stategrid[0])

    print(rows)
    print(cols)
    grid = []

    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(0)

    return grid

# def resetStateMatrix(template_matrix):
#     for i in range(len(state_matrix)):
#         for j in range(len(state_matrix[0])):
#             state_matrix[i][j] = template_matrix[i][j]

def getState(state_matrix, pos_x, pos_y):
    if (pos_x < 0 or pos_x >= len(state_matrix)):
        return None
    if (pos_y < 0 or pos_y >= len(state_matrix[0])):
        return None

    return state_matrix[pos_x][pos_y]

#input is state at each direction
def pairStateAction(possible_states):
    stateaction = []
    #keep order
    if (possible_states[0] != None):
        stateaction.append({"state": possible_states[0], "action": "left"})
    if (possible_states[1] != None):
        stateaction.append({"state": possible_states[1], "action": "right"})
    if (possible_states[2] != None):
        stateaction.append({"state": possible_states[2], "action": "up"})
    if (possible_states[3] != None):
        stateaction.append({"state": possible_states[3], "action": "down"})
    return stateaction

#x and y might not be the right descriptors, because the movement calculations are 
#backwards
def getActionPos(x,y,action):
    if (action == "left"):
        return x, y-1
    if (action == "right"):
        return x, y+1
    if (action == "up"):
        return x-1, y
    if (action == "down"):
        return x+1, y

#
#
def chooseStateAction(stateaction,randomrate):
    threshold = randomrate
    israndom = random.random()
    #random choice
    if (israndom < threshold):
        choice = random.randint(0, len(stateaction) - 1)
        return stateaction[choice]["state"], stateaction[choice]["action"]
    #calculated choice
    else:
        #max q value?
        max = float("-inf")
        for i in range(len(stateaction)):
            state = stateaction[i]["state"]
            action = stateaction[i]["action"]
            q_val = q_table[state][action]
            if (q_val > max):
                max = q_val
                fin_state = state
                fin_act = action

        return fin_state, fin_act

#
#
def performAction(x, y, state, curr_score):
    return x, y, curr_score + state_score[state]

#
#                
def getDelta(state_matrix, curr_score, pos_x, pos_y, future_states):
    #get current
    discount = 0.85 #not sure
    current = state_matrix[pos_x][pos_y]
    reward = state_score[current]
    #get possible future options
    stateaction = pairStateAction(future_states)
    
    #find max future path
    max = 0
    for i in range(len(stateaction)):
        state = stateaction[i]["state"]
        action = stateaction[i]["action"]
        if (q_table[state][action] > max):
            max = q_table[state][action]

    return reward + (discount * max) - curr_score

def updateQTable(state_matrix, state, action, pos_x, pos_y):
     alpha = 0.6
     curr_score = q_table[state][action]
     future_states = getFutureStates(state_matrix, pos_x,pos_y)

     return curr_score + (alpha * getDelta(state_matrix, curr_score, pos_x, pos_y, future_states))

#keep order
def getFutureStates(state_matrix, pos_x, pos_y):
    future_states = []
    left = getState(state_matrix, pos_x, pos_y-1)
    right = getState(state_matrix, pos_x, pos_y+1)
    up = getState(state_matrix, pos_x-1, pos_y)
    down = getState(state_matrix, pos_x+1, pos_y)

    #possible actions array
    future_states = []
    future_states.append(left)
    future_states.append(right)
    future_states.append(up)
    future_states.append(down)

    return future_states

def runMazeSolver(state_matrix, x,y,max_steps, randomrate, initscore):
    pos_x = x
    pos_y = y
    score = initscore
    max_steps = max_steps
    record = []

    for step in range(max_steps):
        cur_state = state_matrix[pos_x][pos_y]

        if (cur_state == "goal" or cur_state == "nogo"):
            break

        # print("Before:" + state_matrix[pos_x][pos_y])

        #check states can only be used once
        if (cur_state == "check"):
            state_matrix[pos_x][pos_y] = "blank"

        # print("After:" + state_matrix[pos_x][pos_y])

        #keep order
        #possible actions
        possible_states = getFutureStates(state_matrix, pos_x, pos_y)

        #choose action 
        stateaction = pairStateAction(possible_states)
        state, action = chooseStateAction(stateaction, randomrate)

        upd_x,upd_y = getActionPos(pos_x, pos_y, action)
        #update current score and position
        pos_x, pos_y, score = performAction(upd_x, upd_y, state, score)

        #seems backwards but its not
        record.append("Step: " + str(step) + ", " + str(pos_y) + " " + str(pos_x) + " " + state)

        #update q_table
        q_table[state][action] = updateQTable(state_matrix, state, action, pos_x, pos_y)

    return score, record

#set the matrix to navigate through
#state_matrix = complex_one_path
solver_tries = 100

# test = createOccuranceGrid(state_matrix)
# print(test)

for i in range(solver_tries):
    print("Try: " + str(i))
    #print(complex_one_path_good_test)
    matrix = copy.deepcopy(complex_one_path_good_test)
    score, results = runMazeSolver(matrix,0,0,1000,0.4,100)
    #print(state_matrix)
    print(results)
    print(score)

#final informed try
matrix = copy.deepcopy(complex_one_path_good_test)
score, results = runMazeSolver(matrix,0,0,100,0,100)
print(results)
print(score)
print(q_table)
