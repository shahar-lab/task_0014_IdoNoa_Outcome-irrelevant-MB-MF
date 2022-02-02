from numpy.random import choice
from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
import numpy as np
import pandas as pd


def game_pause_func(window, game_pause):
    window.flip(clearBuffer=True)
    game_pause.draw()
    window.update()
    event.waitKeys(keyList=["space"])


def update_data_ch2(data_file_vars, key1, rt1, selected_person):
    data_file_vars["key1"] = key1
    data_file_vars["rt1"] = rt1
    data_file_vars["selected_person"] = selected_person

    return data_file_vars


def save_data(data_file, data_file_vars):
    subject_num = data_file_vars["subject_num"]
    block_type = data_file_vars["block_type"]
    block = data_file_vars["block"]
    t = data_file_vars["t"]
    person_pair = data_file_vars["person_pair"]
    fruit = data_file_vars["fruit_list"]
    wear = data_file_vars["wear_list"]
    number_of_trials_in_block = data_file_vars["number_of_trials_in_block"]
    r1 = data_file_vars["r1"]
    r2 = data_file_vars["r2"]
    r3 = data_file_vars["r3"]
    r4 = data_file_vars["r4"]
    iti = data_file_vars["iti"]
    selected_person = data_file_vars["selected_person"]
    person_pair = data_file_vars["person_pair"]
    key1 = data_file_vars["key1"]
    rt1 = data_file_vars["rt1"]
    key2 = data_file_vars["key2"]
    rt2 = data_file_vars["rt2"]
    key3 = data_file_vars["key3"]
    rt3 = data_file_vars["rt3"]
    fruit_reward = data_file_vars["fruit_reward"]
    fruit_reward_probs = data_file_vars["fruit_reward_probs"]
    wear_reward = data_file_vars["wear_reward"]
    wear_reward_probs = data_file_vars["wear_reward_probs"]
    first_product = data_file_vars["first_product"]
    second_product = data_file_vars["second_product"]
    fruit_loc = data_file_vars["fruit_loc"]
    wear_loc = data_file_vars["wear_loc"]
    left_person_fruit = int(fruit[person_pair[0]][8])
    left_person_wear = int(wear[person_pair[0]][8])
    right_person_fruit = int(fruit[person_pair[1]][8])
    right_person_wear = int(wear[person_pair[1]][8])
    if pd.isna(selected_person):
        ch_person_fruit = np.nan
        ch_person_wear = np.nan
        exp_value_ch_fruit = np.nan
        exp_value_ch_wear = np.nan
    else:
        ch_person_fruit = int(fruit[selected_person][8])
        ch_person_wear = int(wear[selected_person][8])
        exp_value_ch_fruit = fruit_reward_probs[selected_person]
        exp_value_ch_wear = wear_reward_probs[selected_person]
    # full print
    data_file.write(
        "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%s,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
        % (
            # general
            subject_num,  # f
            block_type,  # s
            block + 1,  # f starts in 1
            t + 1,  # f starts in 1
            # choice
            person_pair[0] + 1,  # f  1-4
            left_person_fruit,  # f
            left_person_wear,  # f
            person_pair[1] + 1,  # f right_person 1-4
            right_person_fruit,  # f right_person_fruit
            right_person_wear,  # f right_person_wear
            selected_person + 1,  # f ch_person
            ch_person_fruit,  # f ch_person_fruit
            ch_person_wear,  # f ch_person_wear
            key1,  # s key1
            rt1,  # f rt1
            # outcomes
            exp_value_ch_fruit,  # f  exp_value_ch_fruit
            fruit_reward,  # f reward_fruit
            exp_value_ch_wear,  # f exp_value_ch_wear
            wear_reward,  # f reward_ch_wear
            key2,  # s key2
            rt2,  # f rt2
            key3,  # s key3
            rt3,  # f rt3
            first_product,  # s first_product (fruit/wear)
            second_product,  # s second_product (fruit/wear)
            fruit_loc,  # s fruit_loc
            r1[t + block * number_of_trials_in_block],  # f exp_value_fruit1
            r2[t + block * number_of_trials_in_block],  # f exp_value_fruit2
            wear_loc,  # s wear_loc
            r3[t + block * number_of_trials_in_block],  # f exp_value_wear1
            r4[t + block * number_of_trials_in_block],  # f exp_value_wear2
            iti,  # f iti
        )
    )


def instructions(window, num_instructions, file_location):
    # file location is the place where the pictures are at
    for instruction in range(1, num_instructions + 1):
        test_instructions = visual.ImageStim(
            window,
            image=file_location + str(instruction) + ".png",
            pos=[0, 0],
            interpolate=True,
        )
        test_instructions.draw()
        window.update()
        event.waitKeys(keyList=["space", "s", "k"])


def quiz(window, num_questions, file_location):
    # quiz
    start_quiz = visual.ImageStim(
        window,
        image="instructions/instructions_test/start_quiz" + ".png",
        pos=[0, 0],
        interpolate=True,
    )
    start_quiz.draw()
    window.update()
    event.waitKeys(keyList=["space"])

    answers = ["s", "s", "k", "s", "k"]
    for question in range(1, num_questions + 1):
        quiz = visual.ImageStim(
            window,
            image=file_location + str(question) + ".png",
            pos=[0, 0],
            interpolate=True,
        )
        quiz.draw()
        window.update()
        event.waitKeys(keyList=answers[question - 1])


def start_training(
    window, file_location="instructions/instructions_test/start_training.png"
):
    # training
    start_training = visual.ImageStim(
        window, image=file_location, pos=[0, 0], interpolate=True,
    )
    start_training.draw()
    window.update()
    event.waitKeys(keyList=["space"])


def start_test(window, file_location="instructions/instructions_test/start_test.png"):
    start_test = visual.ImageStim(
        window, image=file_location, pos=[0, 0], interpolate=True,
    )
    # test
    start_test.draw()
    window.update()
    event.waitKeys(keyList=["space"])


def finish_test(window, file_location="instructions/instructions_test/finish_test.png"):
    finish_test = visual.ImageStim(
        window, image=file_location, pos=[0, 0], interpolate=True,
    )
    finish_test.draw()
    window.update()
    event.waitKeys(keyList=["space"])


def update_data_full(
    data_file_vars,
    first_product,
    second_product,
    key1,
    rt1,
    key2,
    rt2,
    key3,
    rt3,
    selected_person,
    fruit_reward,
    wear_reward,
    fruit_reward_probs,
    wear_reward_probs,
):
    data_file_vars["key1"] = key1
    data_file_vars["rt1"] = rt1
    data_file_vars["key2"] = key2
    data_file_vars["rt2"] = rt2
    data_file_vars["key3"] = key3
    data_file_vars["rt3"] = rt3
    data_file_vars["selected_person"] = selected_person
    data_file_vars["first_product"] = first_product
    data_file_vars["second_product"] = second_product
    data_file_vars["fruit_reward"] = fruit_reward
    data_file_vars["fruit_reward_probs"] = fruit_reward_probs
    data_file_vars["wear_reward"] = wear_reward
    data_file_vars["wear_reward_probs"] = wear_reward_probs
    return data_file_vars


def update_data_ch3(
    data_file_vars,
    first_product,
    second_product,
    key1,
    rt1,
    key2,
    rt2,
    selected_person,
    fruit_reward,
    wear_reward,
    fruit_reward_probs,
    wear_reward_probs,
):
    data_file_vars["key1"] = key1
    data_file_vars["rt1"] = rt1
    data_file_vars["key2"] = key2
    data_file_vars["rt2"] = rt2
    data_file_vars["selected_person"] = selected_person
    data_file_vars["first_product"] = first_product
    data_file_vars["second_product"] = second_product
    # fill with nans the reward related variables of the second choice object
    if first_product == "fruit":
        data_file_vars["fruit_reward"] = fruit_reward
        data_file_vars["fruit_reward_probs"] = fruit_reward_probs
    else:
        data_file_vars["wear_reward"] = wear_reward
        data_file_vars["wear_reward_probs"] = wear_reward_probs
    return data_file_vars


def draw_first_reward(
    window,
    stimuli_dict,
    first_reward,
    wait_outcome2,
    first_rectangle_loc,
    first_reward_position,
    draw_covers,
    second_rectangle_loc,
    myclock,
):
    # defining the location of the reward
    stimuli_dict["won"].pos = [0, first_reward_position]
    stimuli_dict["lost"].pos = [0, first_reward_position]
    first_reward.draw()
    rect(window, *first_rectangle_loc)
    window.flip()
    core.wait(wait_outcome2)
    draws(*draw_covers)
    rect(window, *second_rectangle_loc)
    window.callOnFlip(myclock.reset)
    window.flip()
    return stimuli_dict


def draw_second_choice_screen(window, wait_ch2, first_rectangle_loc, draw_first_object):
    # draw first object
    draws(*draw_first_object)
    rect(window, *first_rectangle_loc)
    window.flip()
    core.wait(wait_ch2)
    draws(*draw_first_object)


def draw_first_choice_screen(
    window, wait_ch1, myclock, first_rectangle_loc, presented_person, stimuli_dict
):
    fruit_cover = stimuli_dict["fruit_cover"]
    wear_cover = stimuli_dict["wear_cover"]
    # drawing the stimuli
    presented_person.autoDraw = True  # this keeps the presented person on screen
    fruit_cover.draw()
    wear_cover.draw()
    rect(window, -0.7, 0.7, 0.3, 0.7)
    window.flip()
    core.wait(wait_ch1)
    fruit_cover.draw()
    wear_cover.draw()
    rect(window, *first_rectangle_loc)
    window.callOnFlip(myclock.reset)
    window.flip()


def show_objects(stimuli_dict, fruit_reward_stimuli, wear_reward_stimuli):
    fruit_cover = stimuli_dict["fruit_cover"]
    wear_cover = stimuli_dict["wear_cover"]
    fruit_appear_first = stimuli_dict["fruit_appear_first"]
    fruit_stimulus = stimuli_dict["fruit_stimulus"]
    wear_cover = stimuli_dict["wear_cover"]
    fruit_cover = stimuli_dict["fruit_cover"]
    wear_stimulus = stimuli_dict["wear_stimulus"]
    # draw according to counterbalanced order of object appearance
    if fruit_appear_first:
        first_rectangle_loc = (-0.7, 0.7, -0.24, 0.26)
        second_rectangle_loc = (-0.7, 0.7, -0.78, -0.24)
        draw_first_object = (
            fruit_stimulus,
            wear_cover,
        )
        draw_covers = (fruit_cover, wear_cover)
        draw_second_stimulus = (
            fruit_cover,
            wear_stimulus,
        )
        first_reward = fruit_reward_stimuli
        second_reward = wear_reward_stimuli
        first_reward_position = 0
        second_reward_position = -5
        first_object_loc = fruit_stimulus.pos[0]
        second_object_loc = wear_stimulus.pos[0]
        first_product = "fruit"
        second_product = "wear"

    else:
        first_rectangle_loc = (-0.7, 0.7, -0.78, -0.24)
        second_rectangle_loc = (-0.7, 0.7, -0.24, 0.26)
        draw_first_object = (
            fruit_cover,
            wear_stimulus,
        )
        draw_covers = (fruit_cover, wear_cover)
        draw_second_stimulus = (
            fruit_stimulus,
            wear_cover,
        )
        first_reward = wear_reward_stimuli
        second_reward = fruit_reward_stimuli
        first_reward_position = -5
        second_reward_position = 0
        first_object_loc = wear_stimulus.pos[0]
        second_object_loc = fruit_stimulus.pos[0]
        first_product = "wear"
        second_product = "fruit"

    return (
        first_rectangle_loc,
        second_rectangle_loc,
        draw_first_object,
        draw_covers,
        draw_second_stimulus,
        first_reward,
        second_reward,
        first_reward_position,
        second_reward_position,
        first_object_loc,
        second_object_loc,
        first_product,
        second_product,
    )


def draw_second_object_and_reward(
    window,
    stimuli_dict,
    presented_person,
    wait_ch3,
    wait_outcome3,
    second_reward,
    second_reward_position,
    draw_second_stimulus,
    second_rectangle_loc,
):
    draws(*draw_second_stimulus)
    rect(window, *second_rectangle_loc)
    window.flip()
    core.wait(wait_ch3)
    stimuli_dict["won"].pos = [0, second_reward_position]
    stimuli_dict["lost"].pos = [0, second_reward_position]
    draws(*draw_second_stimulus)
    second_reward.draw()
    rect(window, *second_rectangle_loc)
    window.flip()
    core.wait(wait_outcome3)
    draws(*draw_second_stimulus)
    window.flip()
    presented_person.autoDraw = False
    return stimuli_dict, presented_person


def draw_reward(
    r1, r2, r3, r4, t, block, number_of_trials_in_block, selected_person, stimuli_dict
):
    # fruit reward probabilities refers to lines 1 and 2 and wear to lines 3 and 4 in the random walk csv file.
    # to attach reward probabilities to persons, we create the following arrays.
    # we don't reset the reward probabilities in each block, so we take the relevant column from the randomwalk.
    fruit_reward_probs = [
        r1[t + block * number_of_trials_in_block],
        r2[t + block * number_of_trials_in_block],
        r2[t + block * number_of_trials_in_block],
        r1[t + block * number_of_trials_in_block],
    ]
    wear_reward_probs = [
        r3[t + block * number_of_trials_in_block],
        r4[t + block * number_of_trials_in_block],
        r3[t + block * number_of_trials_in_block],
        r4[t + block * number_of_trials_in_block],
    ]

    # check if won/lost by predetermined probablity of selected_person
    if np.random.random() < fruit_reward_probs[selected_person]:
        fruit_reward = 1
        fruit_reward_stimuli = stimuli_dict["won"]
    else:
        fruit_reward = 0
        fruit_reward_stimuli = stimuli_dict["lost"]
    if np.random.random() < wear_reward_probs[selected_person]:
        wear_reward = 1
        wear_reward_stimuli = stimuli_dict["won"]
    else:
        wear_reward = 0
        wear_reward_stimuli = stimuli_dict["lost"]
    return (
        fruit_reward,
        fruit_reward_stimuli,
        fruit_reward_probs,
        wear_reward,
        wear_reward_stimuli,
        wear_reward_probs,
    )


def wrong_key_func(window, wrong_key):
    window.flip(clearBuffer=True)
    wrong_key.draw()
    window.update()
    core.wait(1)


def call_supervisor_func(window, call_supervisor):
    window.flip(clearBuffer=True)
    call_supervisor.draw()
    window.update()
    event.waitKeys(keyList=["space"])
    core.wait(2)


def stimuli_by_choice(keys_event, stimuli_dict, fruit, wear):
    # set the stimulus by the selected choice (left or right)
    # this function updates the stimuli, and creates choice variables
    key1, rt1 = keys_event[0]
    if keys_event[0][0] == "s":
        selected_person = stimuli_dict["person_pair"][0]
        presented_person = stimuli_dict["left_person"]
        stimuli_dict["fruit_stimulus"].image = fruit[selected_person]
        stimuli_dict["wear_stimulus"].image = wear[selected_person]
    elif keys_event[0][0] == "k":
        selected_person = stimuli_dict["person_pair"][1]
        presented_person = stimuli_dict["right_person"]
        stimuli_dict["fruit_stimulus"].image = fruit[selected_person]
        stimuli_dict["wear_stimulus"].image = wear[selected_person]
        # the fruit and wear arrays are organized according to the model, thus choosing fruit[selected_person] gives the selected_person's fruit.
    else:
        selected_person = np.nan
        presented_person = np.nan
    return stimuli_dict, selected_person, presented_person, key1, rt1


def too_slow_func(window, too_slow):
    # if no response was pressed, show "Too Slow" and save current trial to csv
    window.flip(clearBuffer=True)
    too_slow.draw()
    window.update()
    core.wait(1)


def choice(ch_deadline, myclock):
    # wait for person choice
    keys_event = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)
    return keys_event


def draw_stimuli_ch1(window, fixation, stimuli_dict, iti):
    # draw the stimuli and update the window
    window.flip(clearBuffer=True)
    fixation.draw()
    window.update()
    core.wait(iti)
    stimuli_dict["left_person"].draw()
    stimuli_dict["right_person"].draw()
    stimuli_dict["fruit_cover"].draw()
    stimuli_dict["wear_cover"].draw()
    stimuli_dict["fruit_green_base"].draw()
    stimuli_dict["wear_green_base"].draw()
    rect(window, -0.7, 0.7, 0.3, 0.7)
    window.update()


def get_randomwalk(subject_num):
    if subject_num % 2 == 0:
        rwalk = np.genfromtxt("rndwalk/rndwalk2.csv", delimiter=",")
    else:
        rwalk = np.genfromtxt("rndwalk/rndwalk1.csv", delimiter=",")
    r1 = rwalk[0, :]
    r2 = rwalk[1, :]
    r3 = rwalk[2, :]
    r4 = rwalk[3, :]
    return r1, r2, r3, r4


def stimuli(window, person_list, valid_pairs, x_axis_locations):
    stimuli_dict = dict()
    stimuli_dict["person_pair"] = valid_pairs[np.random.choice(8, 1)[0]]
    # draw randomly the locations of the fruit and of the wear
    stimuli_dict["fruit_loc_pxl"] = np.random.choice(x_axis_locations)
    stimuli_dict["wear_loc_pxl"] = np.random.choice(x_axis_locations)
    if stimuli_dict["fruit_loc_pxl"] == -3:  # this is the location on screen
        fruit_loc = "left"
    else:
        fruit_loc = "right"
    stimuli_dict["fruit_loc"] = fruit_loc
    if stimuli_dict["wear_loc_pxl"] == -3:
        wear_loc = "left"
    else:
        wear_loc = "right"
    stimuli_dict["wear_loc"] = wear_loc
    # counterbalance of stimulus presentation - fruit shown first or wear first.
    stimuli_dict["fruit_appear_first"] = np.random.choice(2)

    # define the stimuli according to the raffled pair
    stimuli_dict["left_person"] = visual.ImageStim(
        window,
        image=person_list[stimuli_dict["person_pair"][0]],
        pos=[-6, 5],
        interpolate=True,
    )
    stimuli_dict["right_person"] = visual.ImageStim(
        window,
        image=person_list[stimuli_dict["person_pair"][1]],
        pos=[6, 5],
        interpolate=True,
    )

    stimuli_dict["fruit_stimulus"] = visual.ImageStim(
        window, image=None, pos=[stimuli_dict["fruit_loc_pxl"], 0], size=2
    )
    stimuli_dict["fruit_cover"] = visual.ImageStim(
        window, image="images/fruit_cvr.png", pos=[stimuli_dict["fruit_loc_pxl"], 0]
    )
    stimuli_dict["wear_stimulus"] = visual.ImageStim(
        window, image=None, pos=[stimuli_dict["wear_loc_pxl"], -5], size=2
    )
    stimuli_dict["wear_cover"] = visual.ImageStim(
        window, image="images/wear_cvr.png", pos=[stimuli_dict["wear_loc_pxl"], -5]
    )

    stimuli_dict["fruit_green_base"] = visual.ImageStim(
        window, image="images/greenbase.png", pos=[-stimuli_dict["fruit_loc_pxl"], -0.5]
    )
    stimuli_dict["wear_green_base"] = visual.ImageStim(
        window, image="images/greenbase.png", pos=[-stimuli_dict["wear_loc_pxl"], -6]
    )

    # define won/lost feedback
    stimuli_dict["won"] = visual.ImageStim(
        window, image="images/rw.jpg", pos=[0, 0], size=2, interpolate=True
    )
    stimuli_dict["lost"] = visual.ImageStim(
        window, image="images/ur.jpg", pos=[0, 0], size=2, interpolate=True
    )
    return stimuli_dict


# aborting the experiment if escape is pressed
def abort(window):
    # check keyboard presses
    kb = keyboard.Keyboard()
    kb.start()
    keys = kb.getKeys(["escape"])
    if "escape" in keys:
        window.close()
        core.quit()


# defining the rectangle used to mark selection
def rect(window, x1, x2, y1, y2):
    a = visual.Line(
        window, start=(x1, y1), end=(x2, y1), size=10, lineColor=[1.0, -1, -1]
    )
    b = visual.Line(
        window, start=(x1, y1), end=(x1, y2), size=10, lineColor=[1.0, -1, -1]
    )
    c = visual.Line(
        window, start=(x2, y2), end=(x2, y1), size=10, lineColor=[1.0, -1, -1]
    )
    d = visual.Line(
        window, start=(x2, y2), end=(x1, y2), size=10, lineColor=[1.0, -1, -1]
    )
    a.draw()
    b.draw()
    c.draw()
    d.draw()
    return


# packs the drawing of the objects according to order
def draws(one, two):
    one.draw()
    two.draw()
    return
