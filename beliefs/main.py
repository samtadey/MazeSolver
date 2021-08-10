import random
from environment import getKeyList, advanceTree, build_tree_complete
from environment import two, three, four, build_q_table
from generate_scoring import doHamming, generateStateScore, generateStateOrder, generateStateScore, generateLevelToOrder, generateDiffReward 
    
def next_node(tree_pos, currstate, randomrate):

    if isinstance(tree_pos, str):
        return tree_pos

    next_keys = getKeyList(tree_pos)
    #this is last level
    israndom = random.random()
    #random choice
    if (israndom < randomrate):
        choice = random.randint(0, len(next_keys) - 1)
        return next_keys[choice]
    #calculated choice
    else:
        #max q value?
        max = float("-inf")
        for key in next_keys:
            q_val = q_table[key][currstate]

            if (q_val > max):
                max = q_val
                new = key

        return new

def calcReward(state_score, state_score_order, state_score_diff_reward, current, tree_level):
    reward = state_score[current]
    #get tree level
    #map level to order rank
    place = state_score_order[current]
    level = level_to_order[tree_level]
    print("Expected Level: " + str(place) + " - Placed At: " + str(level))
    #treelevel wrong
    leveldiff = abs(place - level)
    #print(leveldiff)
    #map level to reward
    #print(state_score_diff_reward[leveldiff])

    reward = state_score_diff_reward[leveldiff] * reward
    return reward

def getDelta(state_score, state_score_order, state_score_diff_reward, tree, current, prev, curr_score, level):
    #get current
    discount = 0.5 #not sure
    #calculate reward
    reward = calcReward(state_score, state_score_order, state_score_diff_reward, current, level)

    max = 0

    if isinstance(tree, str):
        return reward + (discount * q_table[tree][prev]) - curr_score

    nnode = getKeyList(tree[current])
    if nnode == None:
        lastleaf = advanceTree(tree, current)
        #print("nnode " + lastleaf)
        return reward + (discount * q_table[lastleaf][current]) - curr_score

    #have to error handle this
    for key in nnode:
        next = key
        if (q_table[next][current] > max):
            max = q_table[next][current]

    return reward + (discount * max) - curr_score


def updateQTable(state_score, state_score_order, state_score_diff_reward, tree, curr, prev, level):
     alpha = 0.6
     curr_score = q_table[curr][prev]

     return curr_score + (alpha * getDelta(state_score, state_score_order, state_score_diff_reward, tree, curr, prev, curr_score, level))



def runMazeSolver(state_score, state_score_order, state_score_diff_reward, tree, curr, randomrate, initscore):
    score = initscore
    record = []

    prev = curr
    state = tree[curr]
    next = 'placeholder'
    level = 1
    while state != None:
        print(level)
        next = next_node(state, prev, randomrate)
        #buildTreeDynamic(matrix, choices,)
        if next == None:
            break
        #print("Prev " + prev + " -> " + next)
        #add breaking condition
        #or change max steps to num states? +1?
        score+=state_score[next]
        #seems backwards but its not
        record.append(str(next))
        #record.append(str(prev) + " -> " + str(next))
        #update q_table
        q_table[next][prev] = updateQTable(state_score, state_score_order, state_score_diff_reward, state, next, prev, level)
        #advance tree
        #if none return
        state = advanceTree(state, next)
        level+=1
        prev = next

    return score, record




#traditional method
def basicMethod(tree, q_table, state_score, level_to_order, state_score_order, state_score_diff_reward):

    solver_tries = 100
    #matrix = {'start': {}}
    for i in range(solver_tries):
        print("Try: " + str(i))
        #reinit choices
        score, results = runMazeSolver(state_score, state_score_order, state_score_diff_reward, tree, "start", 0.3, 100)

    print(q_table)
    print("test")
    score, results = runMazeSolver(state_score, state_score_order, state_score_diff_reward, tree, "start", 0, 100)
    #print(state_matrix)
    print(results)
    print(score)



#create members
q_table = build_q_table(three)
tree = build_tree_complete(three)

bel_arr2 = ["000", "001", "010", "011", "100", "101", "110", "111"]
sent_arr2 = ["000"]

hammingresult = doHamming(bel_arr2, sent_arr2)
state_score = generateStateScore(hammingresult)
level_to_order = generateLevelToOrder(hammingresult)
state_score_order = generateStateOrder(hammingresult)
state_score_diff_reward = generateDiffReward(hammingresult)
#run solver
basicMethod(tree, q_table, state_score, level_to_order, state_score_order, state_score_diff_reward)
