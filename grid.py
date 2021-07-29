state_score = {
    "blank": -5,
    "good": -3,
    "dang": -10, 
    "check": 5,
    "nogo": -200, #end loop
    "goal": 1000, #end loop
}

dis_metric = {
    "blank": -2,
    "good": -2,
    "dang": -2,
    "check": -2,
}

basic_state = [
    ["blank", "good", "dang", "nogo"],
    ["dang", "blank", "good", "nogo"],
    ["nogo", "dang", "blank", "nogo"],
    ["blank", "blank", "good", "dang"],
    ["nogo", "blank", "blank", "blank"],
    ["nogo", "nogo", "good", "goal"]
]

basic_state2 = [
    ["blank", "dang", "blank", "good", "nogo"],
    ["dang", "check", "dang", "check", "nogo"],
    ["nogo", "blank", "dang", "good", "dang"],
    ["nogo", "check", "dang", "check", "nogo"],
    ["nogo", "good", "blank", "good", "good"],
    ["nogo", "check", "dang", "check", "goal"]
]

tradeoff_state = [
    ["blank", "blank", "blank"],
    ["good", "dang", "blank"],
    ["dang", "good", "goal"],
]

complex_state = [
    ["blank", "dang", "nogo", "nogo", "nogo", "nogo", "nogo", "nogo", "nogo", "nogo"],
    ["dang", "check", "blank", "check", "blank", "check", "blank", "check", "good", "nogo"],
    ["nogo", "blank", "dang", "blank", "dang", "blank", "dang", "blank", "dang", "nogo"],
    ["nogo", "check", "good", "check", "nogo", "nogo", "nogo", "check", "blank", "nogo"],
    ["nogo", "dang", "blank", "good", "dang", "blank", "good", "blank", "good", "nogo"],
    ["nogo", "check", "blank", "check", "blank", "check", "blank", "check", "blank", "nogo"],
    ["nogo", "dang", "dang", "dang", "good", "good", "dang", "dang", "dang","nogo"],
    ["nogo", "good", "blank", "check", "blank", "check", "check", "blank", "dang", "nogo"],
    ["nogo", "check", "nogo", "good",  "blank", "good", "dang", "nogo", "nogo", "nogo"],
    ["nogo", "good", "check", "blank", "check", "goal", "check", "nogo", "nogo", "nogo"],
]

complex_one_path = [
    ["blank", "dang", "nogo", "nogo", "nogo", "nogo", "nogo", "nogo", "nogo", "nogo"],
    ["dang", "check", "blank", "check", "blank", "dang", "blank", "blank", "good", "nogo"],
    ["nogo", "blank", "good", "blank", "dang", "blank", "dang", "blank", "dang", "nogo"],
    ["nogo", "dang", "good", "check", "nogo", "nogo", "nogo", "blank", "blank", "nogo"],
    ["nogo", "dang", "blank", "good", "blank", "blank", "good", "blank", "good", "nogo"],
    ["nogo", "dang", "blank", "check", "blank", "check", "blank", "good", "blank", "nogo"],
    ["nogo", "dang", "dang", "dang", "good", "good", "dang", "dang", "dang","nogo"],
    ["nogo", "good", "blank", "blank", "blank", "check", "blank", "blank", "dang", "nogo"],
    ["nogo", "blank", "nogo", "good",  "blank", "good", "blank", "nogo", "nogo", "nogo"],
    ["nogo", "good", "good", "blank", "blank", "goal", "good", "nogo", "nogo", "nogo"],
]

#up,down,left,right
q_table = {
    "blank": {"up": 0, "down": 0, "right": 0, "left": 0},
    "good" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "dang" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "check" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "nogo" : {"up": 0, "down": 0, "right": 0, "left": 0},
    "goal" : {"up": 0, "down": 0, "right": 0, "left": 0},
}