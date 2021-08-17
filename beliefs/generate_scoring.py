import math

#return result beliefstate separated into multiple arrays, by hamming distance
def doHamming(bel_arr, sent_arr):
    set = []
    minset = []

    min = float('inf')
    #find min states
    for state in sent_arr:
        min_dist = minDistance(bel_arr, state)
        if min_dist < min:
            min = min_dist
            minset = []
            minset.append(state)
        elif min_dist == min:
            minset.append(state)

    set.append(minset)
    poss_dist = list(range(1, len(minset[0]) + 1))

    for dist in poss_dist:
        grouping = []
        for bel in bel_arr:
            min = float('inf')
            for sent in sent_arr:
                #find min hamming distance to a sentence state
                d = hammDistance(bel, sent)
                if d < min:
                    min = d
            #if the min distance equals our category distance, add it to the category
            if min == dist:  
                grouping.append(bel)

        set.append(grouping)

    return set

#min distance helper
def minDistance(bel_arr, sent_state):
    min = float('inf')

    for state in bel_arr:
        dist = hammDistance(state, sent_state)
        if dist < min:
            min = dist
        
    return min


#returns the hamming distance between two
#states
def hammDistance(state1, state2):
    if len(state1) != len(state2):
        raise Exception('length')

    dist = 0
    for char in range(0, len(state1)):
        if state1[char] != state2[char]:
            dist+=1 

    return dist

#example return value
#tree level to order value
# level_to_order_two = {
#     1: 1,
#     2: 2,
#     3: 2,
#     4: 3
# }
#pair tree level to hamming ranking
#each list in the hammingset corresponds to a level
def generateLevelToOrder(hammingset):
    treelevel = 1
    level_to_order = {}
    setlevel = 1

    for set in hammingset:
        #print(set)
        for i in range(len(set)):
            level_to_order.update({treelevel: setlevel})
            treelevel+=1
        setlevel+=1

    return level_to_order

#example return value
# state_score_two = {
#     "00": 5,
#     "01": 1, 
#     "10": 10,
#     "11": 5,
# }
def generateStateScore(hammingset):
    initval = 1.0
    compoundval = 2.5
    state_score = {}

    #traverse hammingset in reverse to set the scoring system
    #the last list in the set has the least hamming priority, therefore the smallest score
    setno = 0
    for set in reversed(hammingset):
        for states in set:
            if setno == 0:
               state_score[states] = initval
            else:
                state_score[states] = compoundval
        
        compoundval*=2
        setno+=1

    return state_score

# example return value
# state_score_order_three = {
#     "100": 1,
#     "010": 1,
#     "000": 2,
#     "110": 2,
#     "101": 2,
#     "011": 2,
#     "111": 3,
#     "001": 3,
# }
def generateStateOrder(hammingset):
    state_score_order = {}
    setno = 1

    for set in hammingset:
        for state in set:
            state_score_order[state] = setno
        setno+=1

    return state_score_order

#example return value
# state_score_diff_reward_three = {
#     0: 10, 
#     1: -1, 
#     2: -10,
#     3: -100,
# }
def generateDiffReward(hammingset):
    state_score_diff_reward = {}
    power = 0
    base = 10
    #first is the only positive modifier
    state_score_diff_reward.update({0 : 10})

    for i in range(1, len(hammingset)):
        state_score_diff_reward.update({i : -math.pow(base, power)})
        power+=1

    return state_score_diff_reward





