import random
import copy
from environment import two, three, four, five, test_q_table_three, test_q_table_four, build_q_table, buildStateSpace, generateAllStates, generateModQTable
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

def chooseNext(state, q_table, choices, currentstate, level):
    choice = None
    max = float("-inf")

    for state in choices:
        #q_val = q_table[state][currentstate]
        q_val = q_table[state][level]
        if (q_val > max):
            max = q_val
            choice = state

    return choice

def chooseNextState(state, q_table, choices, currentstate, randomrate, level):
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
        return chooseNext(state, q_table, choices, currentstate, level)


def calcRewardTwo(state_score, state_score_order, state_score_diff_reward, current, level):
    reward = state_score[current]
    #get tree level
    #map level to order rank
    place = state_score_order[current]
    #level = level_to_order[tree_level]
    print("Expected Level: " + str(place) + " - Placed At: " + str(level))

    leveldiff = abs(place - level)

    reward = state_score_diff_reward[leveldiff] * reward
    return reward

def getDeltaTwo(state_score, state_score_order, state_score_diff_reward, current, curr_score, level, choices):
    #get current
    discount = 0.75 #not sure
    #calculate reward
    reward = calcRewardTwo(state_score, state_score_order, state_score_diff_reward, current, level)
    max = 1

    # for state in choices:
    #     if q_table[state][level] > max:
    #         max = q_table[state][level] 
    #     # if (q_table[state][current] > max):
    #     #     max = q_table[state][current]

    return reward + (discount * max) - curr_score


def updateQTableTwo(state_score, state_score_order, state_score_diff_reward, curr, prev, level, choices):
    alpha = 0.6
    #curr_score = q_table[curr][prev]
    curr_score = q_table[curr][level]

    return curr_score + (alpha * getDeltaTwo(state_score, state_score_order, state_score_diff_reward, curr, curr_score, level, choices))

def runMazeSolverTwo(allstates, state_score, state_score_order, state_score_diff_reward, statespace, randomrate, initscore):
    score = initscore
    visited = []

    prev = 'start'
    #state = tree[curr]
    nextstate = None
    level = 1
    #fix
    while len(visited) < len(allstates):
        converted_level = level_to_order[level]
        choices = createChoices(visited, allstates)
        nextstate = chooseNextState(statespace, q_table, choices, prev, randomrate, converted_level)
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

        q_table[nextstate][converted_level] = updateQTableTwo(state_score, state_score_order, state_score_diff_reward, nextstate, prev, converted_level, choices)
        #q_table[nextstate][prev] = updateQTableTwo(state_score, state_score_order, state_score_diff_reward, nextstate, prev, level, choices)
        #advance tree
        #if none return
        #state = advanceTree(state, next)
        level+=1
        prev = nextstate

    return score, visited

#traditional method
def basicMethodTwo(allstates, tree, q_table, state_score, state_score_order, state_score_diff_reward):

    solver_tries = 1000
    #matrix = {'start': {}}
    for i in range(solver_tries):
        print("Try: " + str(i))
        #reinit choices
        score, results = runMazeSolverTwo(allstates, state_score, state_score_order, state_score_diff_reward, tree, 0.5, 100)

    print(q_table)
    print("test")
    score, results = runMazeSolverTwo(allstates, state_score, state_score_order, state_score_diff_reward, tree, 0, 100)
    #print(state_matrix)
    print(results)
    print(score)

states = generateAllStates(4)
#create members
#q_table = build_q_table(states)
q_table = generateModQTable(states, 4)
state = buildStateSpace(states)

#change q_table
#change diff rewards assignment

sent_arr = ["0000", "0100", "1000"]

hammingresult = doHamming(states, sent_arr)
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
