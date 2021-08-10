import random
import copy
from environment import two, three, four, five, build_q_table, buildStateSpace
from generate_scoring import doHamming, generateStateScore, generateStateOrder, generateStateScore, generateLevelToOrder, generateDiffReward 

##
##
##Second try with different state structure
##
##

def contains(set, state):
    for item in set:
        if item == state:
            return True
    return False

def createChoices(visited, allstates):
    choices = []
    for state in allstates:
        if not contains(visited, state):
            choices.append(state)
    return choices

def chooseNext(state, q_table, choices, currentstate):
    choice = None
    max = float("-inf")

    for state in choices:
        q_val = q_table[state][currentstate]
        if (q_val > max):
            max = q_val
            choice = state

    return choice

def chooseNextState(state, q_table, choices, currentstate, randomrate):
    israndom = random.random()
    #random choice
    if (israndom < randomrate):
        if len(choices) == 0:
            return None
        if len(choices) == 1:
            return choices[0]
        choice = random.randint(0, len(choices)-1)
        return choices[choice]
    #calculated choice
    else:
        return chooseNext(state, q_table, choices, currentstate)


def calcRewardTwo(state_score, state_score_order, state_score_diff_reward, current, tree_level):
    reward = state_score[current]
    #get tree level
    #map level to order rank
    place = state_score_order[current]
    level = level_to_order[tree_level]
    print("Expected Level: " + str(place) + " - Placed At: " + str(level))

    leveldiff = abs(place - level)

    reward = state_score_diff_reward[leveldiff] * reward
    return reward

def getDeltaTwo(state_score, state_score_order, state_score_diff_reward, current, curr_score, level, choices):
    #get current
    discount = 0.75 #not sure
    #calculate reward
    reward = calcRewardTwo(state_score, state_score_order, state_score_diff_reward, current, level)
    max = 0

    for state in choices:
        if (q_table[state][current] > max):
            max = q_table[state][current]

    return reward + (discount * max) - curr_score


def updateQTableTwo(state_score, state_score_order, state_score_diff_reward, curr, prev, level, choices):
     alpha = 0.6
     curr_score = q_table[curr][prev]

     return curr_score + (alpha * getDeltaTwo(state_score, state_score_order, state_score_diff_reward, curr, curr_score, level, choices))

def runMazeSolverTwo(allstates, state_score, state_score_order, state_score_diff_reward, statespace, randomrate, initscore):
    score = initscore
    visited = []

    prev = 'start'
    #state = tree[curr]
    nextstate = None
    level = 1
    #fix
    while True:
        choices = createChoices(visited, allstates)
        nextstate = chooseNextState(statespace, q_table, choices, prev, randomrate)
        #next choices
        if nextstate == None:
            break
        choices.remove(nextstate)
        #buildTreeDynamic(matrix, choices,)


        ##
        score+=state_score[nextstate]
        #visited states
        visited.append(str(nextstate))
        #update q_table
        q_table[nextstate][prev] = updateQTableTwo(state_score, state_score_order, state_score_diff_reward, nextstate, prev, level, choices)
        #advance tree
        #if none return
        #state = advanceTree(state, next)
        level+=1
        prev = nextstate

    return score, visited

#traditional method
def basicMethodTwo(allstates, tree, q_table, state_score, state_score_order, state_score_diff_reward):

    solver_tries = 100
    #matrix = {'start': {}}
    for i in range(solver_tries):
        print("Try: " + str(i))
        #reinit choices
        score, results = runMazeSolverTwo(allstates, state_score, state_score_order, state_score_diff_reward, tree, 0.3, 100)

    print(q_table)
    print("test")
    score, results = runMazeSolverTwo(allstates, state_score, state_score_order, state_score_diff_reward, tree, 0, 100)
    #print(state_matrix)
    print(results)
    print(score)

states = three
#create members
q_table = build_q_table(states)
state = buildStateSpace(states)

#change q_table
#change diff rewards assignment

sent_arr2 = ["000"]

hammingresult = doHamming(states, sent_arr2)
state_score = generateStateScore(hammingresult)
level_to_order = generateLevelToOrder(hammingresult)
state_score_order = generateStateOrder(hammingresult)
state_score_diff_reward = generateDiffReward(hammingresult)

basicMethodTwo(states, state, q_table, state_score, state_score_order, state_score_diff_reward)

print("State Score")
print(state_score)
print("Level to Order")
print(level_to_order)
print("State Score Order")
print(state_score_order)
print("Diff Reward")
print(state_score_diff_reward)
