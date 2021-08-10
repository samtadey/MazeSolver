
import copy

two = ["00", "01", "10", "11"]
three = ["000", "001", "010", "011", "100", "101", "110", "111"]
four = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
five = ["00000", "00001", "00010", "00011", "00100", "00101", "00110", "00111", "01000", "01001", "01010", "01011", "01100", "01101", "01110",
    "01111", "10000", "10001", "10010", "10011", "10100", "10101", "10110", "10111", "11000", "11001", "11010", "11011", "11100", "11101", "11110", "11111"]


test_q_table_three = {
    "000": {1: 0, 2: 0, 3: 0},
    "001": {1: 0, 2: 0, 3: 0},
    "010": {1: 0, 2: 0, 3: 0},
    "011": {1: 0, 2: 0, 3: 0},    
    "100": {1: 0, 2: 0, 3: 0},
    "101": {1: 0, 2: 0, 3: 0},
    "110": {1: 0, 2: 0, 3: 0},
    "111": {1: 0, 2: 0, 3: 0},
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



