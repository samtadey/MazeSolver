import random


state_score = {
    "blank": -5,
    "good": -1,
    "dang": -10, # 
    "nogo": -200, #end loop
    "goal": 100, #end loop
}

state_matrix = [
    ["blank", "good", "dang", "nogo"],
    ["dang", "blank", "good", "nogo"],
    ["nogo", "dang", "blank", "nogo"],
    ["blank", "blank", "good", "dang"],
    ["nogo", "blank", "blank", "blank"],
    ["nogo", "nogo", "good", "goal"]
]

# state_matrix = [
#     ["blank", "good", "blank", "good", "nogo"],
#     ["nogo", "dang", "good", "blank", "nogo"],
#     ["nogo", "blank", "dang", "good", "dang"],
#     ["nogo", "blank", "good", "blank", "nogo"],
#     ["nogo", "good", "blank", "dang", "good"],
#     ["nogo", "good", "blank", "good", "goal"]
# ]

#up,down,left,right
q_table = {
    "blank": {"up": 0, "down": 0, "right": 0, "left": 0},
    "good" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "dang" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "nogo" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "goal" : {"up": 0, "down": 0, "right": 0, "left": 0},
}

def getState(pos_x, pos_y):
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

def chooseStateAction(stateaction,randomrate):
    threshold = randomrate
    israndom = random.random()
    #random choice
    if (israndom < threshold):
        print("random")
        choice = random.randint(0, len(stateaction) - 1)
        return stateaction[choice]["state"], stateaction[choice]["action"]
    #calculated choice
    else:
        print("greedy")
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

def performAction(x, y, state, curr_score):
    return x, y, curr_score + state_score[state]
                
def getDelta(curr_score, pos_x, pos_y, future_states):
    #get current
    discount = 0.3 #not sure
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

def updateQTable(state, action, pos_x, pos_y):
     alpha = 0.6
     curr_score = q_table[state][action]
     future_states = getFutureStates(pos_x,pos_y)

     return curr_score + (alpha * getDelta(curr_score, pos_x, pos_y, future_states))

#keep order
def getFutureStates(pos_x, pos_y):
    future_states = []
    left = getState(pos_x, pos_y-1)
    right = getState(pos_x, pos_y+1)
    up = getState(pos_x-1, pos_y)
    down = getState(pos_x+1, pos_y)

    #possible actions array
    future_states = []
    future_states.append(left)
    future_states.append(right)
    future_states.append(up)
    future_states.append(down)

    return future_states

def runMazeSolver(x,y,max_steps, randomrate, initscore):
    pos_x = x
    pos_y = y
    score = initscore
    max_steps = max_steps
    record = []

    for step in range(max_steps):
        print("starting step")
        cur_state = state_matrix[pos_x][pos_y]

        if (cur_state == "goal" or cur_state == "nogo"):
            break

        #keep order
        #possible actions
        possible_states = getFutureStates(pos_x, pos_y)

        #choose action 
        stateaction = pairStateAction(possible_states)
        state, action = chooseStateAction(stateaction, randomrate)
        upd_x,upd_y = getActionPos(pos_x, pos_y, action)
        #update current score and position
        pos_x, pos_y, score = performAction(upd_x, upd_y, state, score)
        #seems backwards but its not
        record.append("Step: " + str(step) + ", " + str(pos_y) + " " + str(pos_x) + " " + state)

        #update q_table
        q_table[state][action] = updateQTable(state, action, pos_x, pos_y)

    return score, record


solver_tries = 50

for i in range(solver_tries):
    print("Try: " + str(i))
    score, results = runMazeSolver(0,0,50,0.4,100)
    print(results)
    print(score)

#final informed try
score, results = runMazeSolver(0,0,150,0,100)
print(results)
print(score)
print(q_table)
