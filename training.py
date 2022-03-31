from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
import random, serial, time
from random import sample
import numpy as np
from utils import *


# create a text file to save data
monitor_size = monitors.Monitor("testMonitor").getSizePix()
expInfo = {"subject": "999"}
dlg = gui.DlgFromDict(expInfo, title="Two-armed bandit task")
fileName = "training_for_rani_task_" + expInfo["subject"] + "_" + data.getDateStr()
subject_num = int(expInfo["subject"])
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write(
    "subject,repetition, trial, presented_person, sampled_stimulus, correct_stimulus_location, wrong_stimulus, wrong_stimulus_location, pressed_key, reaction_time\n"
)
window = visual.Window(
    monitor="testMonitor", units="deg", screen=0, color=(255, 255, 255), fullscr=True
)
window.mouseVisible = False

human_list = np.array(
    ["images/m1.png", "images/m2.png", "images/w1.png", "images/w2.png",]
)

fruit_list = np.array(
    ["images/f1.png", "images/f2.png", "images/f2.png", "images/f1.png"]
)

wear_list = np.array(
    ["images/c1.png", "images/c2.png", "images/c1.png", "images/c2.png",]
)
fixation = visual.TextStim(window, text="+", pos=[0, 0], color=(0, 0, 0))
memory_refresh = visual.ImageStim(
    window,
    image="instructions/instructions_training/refresh_memory.png",
    pos=[0, 0],
    interpolate=True,
)

kb = keyboard.Keyboard()
kb.start()
num_instructions = 4
for instruction in range(1, num_instructions + 1):
    prac_instructions = visual.ImageStim(
        window,
        image="instructions/instructions_training/Training" + str(instruction) + ".png",
        pos=[0, 0],
        interpolate=True,
    )
    prac_instructions.draw()
    window.update()
    event.waitKeys(keyList=["space", "s", "k"])

number_of_trials = 16
# defining repetitive objects
too_slow = visual.TextStim(
    window,
    text="Too slow, the task is started from the beginning.",
    pos=[0, 0],
    color=(0, 0, 0),
)
wrong_choice = visual.TextStim(
    window,
    text=("Wrong choice, the task is started from the beginning"),
    pos=[0, 0],
    color=(0, 0, 0),
)
good_choice = visual.TextStim(window, text=("Good job!"), pos=[0, 0], color=(0, 0, 0))

# defining the full lists on which the loop will run
human_loop = np.tile(human_list, int(number_of_trials / len(human_list)))
fruit_loop = np.tile(fruit_list, int(number_of_trials / len(fruit_list)))
wear_loop = np.tile(wear_list, int(number_of_trials / len(wear_list)))

continue_training = True
repetitions = 0
while continue_training == True:  # this loop does the training
    repetitions += 1
    for trial in range(number_of_trials):
        abort(window)
        random_locs = np.random.choice([4, -4], 2, replace=False)
        sampled_person = visual.ImageStim(window, image=human_loop[trial], pos=[0, 5])
        correct_stimulus = visual.ImageStim(
            window,
            image=np.random.choice([fruit_loop[trial], wear_loop[trial]]),
            pos=[random_locs[0], 0],
        )

        # get the possible wrong stimuli (food or wear)
        list_of_wrong_stimuli = [
            np.unique(fruit_loop[fruit_loop != fruit_loop[trial]])[0],
            np.unique(wear_loop[wear_loop != wear_loop[trial]])[0],
        ]

        wrong_stimulus = visual.ImageStim(
            window,
            image=np.random.choice(list_of_wrong_stimuli),
            pos=[random_locs[1], 0],
        )

        counter = visual.TextStim(
            window,
            text=(str(trial + 1) + "/" + str(number_of_trials)),
            pos=[0, -5],
            height=0.5,
            color=(0, 0, 0),
        )
        if random_locs[0] == (-4):
            true_loc = ["s"]
        else:
            true_loc = ["k"]

        fixation.draw()
        window.update()
        core.wait(0.5)
        counter.autoDraw = True
        sampled_person.draw()
        correct_stimulus.draw()
        wrong_stimulus.draw()
        window.update()
        myclock = core.Clock()
        choice = event.waitKeys(maxWait=8)
        RT = myclock.getTime()
        print(RT)
        counter.autoDraw = False
        human_data = sampled_person.image[-6:-4]
        correct_stimulus_data = correct_stimulus.image[-6:-4]
        wrong_stim_data = wrong_stimulus.image[-6:-4]
        dataFile.write(
            "%i,%i,%i,%s,%s,%i,%s,%i,%s,%i\n"
            % (
                subject_num,
                repetitions,
                trial,
                human_data,
                correct_stimulus_data,
                random_locs[0],
                wrong_stim_data,
                random_locs[1],
                choice,
                RT * 1000,
            )
        )
        # check if correct and fast enough
        if choice == true_loc and RT <= 2.5:
            sampled_person.draw()
            correct_stimulus.draw()
            window.update()
            core.wait(1)
            good_choice.draw()
            window.update()
            core.wait(1.0)
            # Time to finish running
            if trial == number_of_trials - 1:
                continue_training = False
        elif RT >= 2.5:  # too slow
            too_slow.draw()
            window.update()
            core.wait(1)
            break
        else:  # wrong choice
            wrong_choice.draw()
            window.update()
            core.wait(1)
            break
    if repetitions % 3 == 0:
        memory_refresh.draw()
        window.update()
        event.waitKeys(keyList=["space"])


finish_training = visual.ImageStim(
    window,
    image="instructions/instructions_training/Training5.png",
    pos=[0, 0],
    interpolate=True,
)
finish_training.draw()
window.update()
event.waitKeys(keyList=["space"])

