from numpy.random import choice
from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
from utils import *
from mytrials import *
import numpy as np

# get subject_num
expInfo = {"subject": "999"}
dlg = gui.DlgFromDict(expInfo, title="Two-armed bandit task")  # update expInfo
subject_num = int(expInfo["subject"])

# create a text file to save data
fileName = "rani_task" + expInfo["subject"] + "_" + data.getDateStr()
data_file = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'

data_file.write(
    "subject,block_type,block,trial, left_person,left_person_fruit,left_person_wear, right_person,right_person_fruit,right_person_wear, ch_person,ch_fruit,ch_wear,keypress1, rt1, exp_value_ch_fruit, reward_fruit, exp_value_ch_wear, reward_wear, keypress2, rt2, keypress3, rt3,first_product,second_product, fruit_location,exp_value_fruit1,exp_value_fruit2,wear_location,exp_value_wear1,exp_value_wear2,iti\n"
)

# create window display
monitor_size = monitors.Monitor("testMonitor").getSizePix()
window = visual.Window(
    monitor="testMonitor",
    screen=0,
    units="deg",
    color=(255, 255, 255),
    fullscr=True,
    allowStencil=True,
)
window.mouseVisible = False

# declaration of persons' and objects' pictures
person_list = [
    "images/m1.png",
    "images/m2.png",
    "images/w1.png",
    "images/w2.png",
]  # those arrays are organized according to the model. m1 has f1 and c1, w2 has f1 and c2...
fruit_list = [
    "images/f1.png",
    "images/f2.png",
    "images/f2.png",
    "images/f1.png",
]  # f1 is bannana, f2 is orange
wear_list = [
    "images/c1.png",
    "images/c2.png",
    "images/c1.png",
    "images/c2.png",
]  # c refers to clothing, c1 is hat, c2 is shirt.

# only pairs of persons who share an object are valid, irrespictable of location
valid_pairs = np.array([[0, 2], [2, 0], [0, 3], [3, 0], [1, 2], [2, 1], [1, 3], [3, 1]])

# locations in pixels units referring to left or right locations of objects
x_axis_locations = [
    3,
    -3,
]

# declaration of visual components
fixation = visual.TextStim(window, text="+", pos=[0, 0], color=(0, 0, 0))
too_slow = visual.TextStim(window, text="Too Slow", pos=[0, 0], color=(0, 0, 0))
wrong_key = visual.TextStim(window, text="Wrong Key", pos=[0, 0], color=(0, 0, 0))
call_supervisor = visual.TextStim(
    window, text="Call supervisor", pos=[0, 0], color=(0, 0, 0)
)
game_pause = visual.ImageStim(
    window,
    image="instructions/instructions_test/game_pause.png",
    pos=[0, 0],
    interpolate=True,
)

# random walk is counterbalanced according to subject_num
r1, r2, r3, r4 = get_randomwalk(subject_num)

# for loop running on the number of blocks
instructions(
    window, num_instructions=14, file_location="instructions/instructions_test/Test"
)
quiz(window, num_questions=5, file_location="instructions/quiz/quiz")

start_training(window)

params_training = {
    "subject_num": subject_num,
    "block_type": "training",
    "number_of_blocks": 1,
    "number_of_trials_in_block": 3,
    "iti": 1,
    "ch_deadline": 6,
    "wait_ch1": 0.5,
    "wait_ch2": 0.5,
    "wait_ch3": 0.5,
    "wait_outcome2": 1,
    "wait_outcome3": 1,
    "r1": r1,
    "r2": r2,
    "r3": r3,
    "r4": r4,
    "person_list": person_list,
    "valid_pairs": valid_pairs,
    "fruit_list": fruit_list,
    "wear_list": wear_list,
    "fixation": fixation,
    "too_slow": too_slow,
    "wrong_key": wrong_key,
    "call_supervisor": call_supervisor,
    "game_pause": game_pause,
    "x_axis_locations": x_axis_locations,
}
# starts training trails
mytrials(window, params_training, data_file)

params_test = {
    "subject_num": subject_num,
    "block_type": "test",
    "number_of_blocks": 3,
    "number_of_trials_in_block": 3,
    "iti": 1,
    "ch_deadline": 6,
    "wait_ch1": 0.5,
    "wait_ch2": 0.5,
    "wait_ch3": 0.5,
    "wait_outcome2": 1,
    "wait_outcome3": 1,
    "r1": r1,
    "r2": r2,
    "r3": r3,
    "r4": r4,
    "person_list": person_list,
    "valid_pairs": valid_pairs,
    "fruit_list": fruit_list,
    "wear_list": wear_list,
    "fixation": fixation,
    "too_slow": too_slow,
    "wrong_key": wrong_key,
    "call_supervisor": call_supervisor,
    "game_pause": game_pause,
    "x_axis_locations": x_axis_locations,
}

start_test(window)
# starts test trails
mytrials(window, params_test, data_file)

finish_test(window)

