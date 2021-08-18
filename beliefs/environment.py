import math
import copy

two = ["00", "01", "10", "11"]
three = ["000", "001", "010", "011", "100", "101", "110", "111"]
four = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
five = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111", "01000", "01001", "01010", "01011", "01100", "01101", "01110",
    "01111", "10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001", "11010", "11011", "11100", "11101", "11110", "11111"]

def changeVal(binary_val):
    if binary_val == '0':
        return '1'
    return '0'

def generateAllStates(num_vars):
    states = []
    total_states = math.pow(2, num_vars)
    binary_switcher = total_states / 2
    var = '0'

    #initiate empty states
    for i in range(int(total_states)):
        states.append("")

    #build state strings 
    for character in range(num_vars):
        counter = 1
        newstrings = []
        for string in states:
            newstring = string.replace(string, string + var)
            newstrings.append(newstring)
            if counter == binary_switcher:
                var = changeVal(var)
                counter = 0
            counter+=1

        #transfer states from the temp object to the state object
        states = []
        for string in newstrings:
            states.append(string)
        
        #
        binary_switcher/=2

    return states

def generateModQTable(states, num_vars):
    q_table = {}

    for state in states:
        q_table[state] = {}
        for i in range(1, num_vars+2):
            q_table[state].update({i:0})

    return q_table

test_q_table_three = {
    "000": {1: 0, 2: 0, 3: 0, 4: 0},
    "001": {1: 0, 2: 0, 3: 0, 4: 0},
    "010": {1: 0, 2: 0, 3: 0, 4: 0},
    "011": {1: 0, 2: 0, 3: 0, 4: 0},    
    "100": {1: 0, 2: 0, 3: 0, 4: 0},
    "101": {1: 0, 2: 0, 3: 0, 4: 0},
    "110": {1: 0, 2: 0, 3: 0, 4: 0},
    "111": {1: 0, 2: 0, 3: 0, 4: 0},
}


{
    '000': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '001': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '010': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '011': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '100': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '101': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '110': {1: 0, 2: 0, 3: 0, 4: 0}, 
    '111': {1: 0, 2: 0, 3: 0, 4: 0}
}

test_q_table_four = {
    "0000": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "0001": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "0010": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "0011": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},  
    "0100": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "0101": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "0110": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "0111": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1000": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1001": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1010": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1011": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1100": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1101": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1110": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    "1111": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},    
}

test_rewards_three = {
    0: 100,
    1: 10,
    2: -10,
    3: -100,
}

#
#Returns next list of keys or None if no new keys
#
def getKeyList(tree):
    try: 
        return list(tree.keys())
    except AttributeError:
        return None

def advanceTree(tree, next):
    try:
        return tree[next]
    except TypeError:
        return None



def build_tree_complete(states):
    tree = { "start": {} }
    build_tree(tree["start"], states, 1)
    return tree


def build_tree(tree, states, justfortesting):
    nextcopy = copy.deepcopy(states)
    #print(nextcopy)

    if (len(states) == 2):
        tree[states[0]] = states[1]
        tree[states[1]] = states[0]
        return

    for key in states:
        tree[key] = {}
        nextcopy = copy.deepcopy(states)
        nextcopy.remove(key)
        build_tree(tree[key], nextcopy, justfortesting+1)
        if justfortesting == 1:
            print(key)


#new state structure



def buildStateSpace(states):
    statespace = {}

    for state1 in states:
        #statespace[state1] = {}
        choices = []
        for state2 in states:
            if state1 != state2:
                choices.append(state2)
        statespace[state1] = choices

    return statespace


# q_table_three = {
#     "000": {"start": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": 0},
# }
def build_q_table(states):
    q_table = {}

    for state in states:
        q_table[state] = {"start": 0}
        for i in range(len(states)):
            if state != states[i]:
                q_table[state].update({states[i]: 0})

    return q_table




