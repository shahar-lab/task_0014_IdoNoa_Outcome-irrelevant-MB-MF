from numpy.random import choice
from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
from utils import *
import numpy as np

# This function runs a loop of trials
def mytrials(window, params, data_file):
    subject_num = params["subject_num"]
    block_type = params["block_type"]
    number_of_blocks = params["number_of_blocks"]
    number_of_trials_in_block = params["number_of_trials_in_block"]
    iti = params["iti"]
    ch_deadline = params["ch_deadline"]
    wait_ch1 = params["wait_ch1"]
    wait_ch2 = params["wait_ch2"]
    wait_ch3 = params["wait_ch3"]
    wait_outcome2 = params["wait_outcome2"]
    wait_outcome3 = params["wait_outcome3"]
    r1 = params["r1"]
    r2 = params["r2"]
    r3 = params["r3"]
    r4 = params["r4"]
    person_list = params["person_list"]
    valid_pairs = params["valid_pairs"]
    fruit_list = params["fruit_list"]
    wear_list = params["wear_list"]
    fixation = params["fixation"]
    too_slow = params["too_slow"]
    wrong_key = params["wrong_key"]
    call_supervisor = params["call_supervisor"]
    game_pause = params["game_pause"]
    x_axis_locations = params["x_axis_locations"]
    for block in range(number_of_blocks):

        # making pauses on every start of block which is not the first
        if block != 0:
            game_pause_func(window, game_pause)
        # for loop running on each trial
        for t in range(number_of_trials_in_block):
            window.flip(clearBuffer=True)
            # abort if esc is pressed
            abort(window)
            # get stimuli
            stimuli_dict = stimuli(window, person_list, valid_pairs, x_axis_locations)
            draw_stimuli_ch1(window, fixation, stimuli_dict, iti)

            # define data
            data_file_vars = {
                "subject_num": subject_num,
                "block_type": block_type,
                "block": block,
                "number_of_trials_in_block": number_of_trials_in_block,
                "t": t,
                "fruit_list": fruit_list,
                "wear_list": wear_list,
                "r1": r1,
                "r2": r2,
                "r3": r3,
                "r4": r4,
                "iti": iti,
                "person_pair": stimuli_dict["person_pair"],
                "fruit_loc": stimuli_dict["fruit_loc"],
                "wear_loc": stimuli_dict["wear_loc"],
                "selected_person": np.nan,
                "key1": np.nan,
                "rt1": np.nan,
                "key2": np.nan,
                "rt2": np.nan,
                "key3": np.nan,
                "rt3": np.nan,
                "fruit_reward": np.nan,
                "fruit_reward_probs": [np.nan, np.nan, np.nan, np.nan],
                "wear_reward": np.nan,
                "wear_reward_probs": [np.nan, np.nan, np.nan, np.nan],
                "first_product": np.nan,
                "second_product": np.nan,
            }
            # choice
            myclock = core.Clock()
            keys_event_ch1 = choice(ch_deadline, myclock)

            # nothing was pressed
            if keys_event_ch1 == None:
                too_slow_func(window, too_slow)
                save_data(data_file, data_file_vars)
                continue

            # if space was pressed it means the participants wanted a break
            elif keys_event_ch1[0][0] == "space":
                call_supervisor_func(window, call_supervisor)
                save_data(data_file, data_file_vars)
                continue

            # a wrong key was pressed
            elif keys_event_ch1[0][0] != "s" and keys_event_ch1[0][0] != "k":
                wrong_key_func(window, wrong_key)
                save_data(data_file, data_file_vars)
                continue

            # get choice variables
            (
                stimuli_dict,
                selected_person,
                presented_person,
                key1,
                rt1,
            ) = stimuli_by_choice(keys_event_ch1, stimuli_dict, fruit_list, wear_list)
            (
                fruit_reward,
                fruit_reward_stimuli,
                fruit_reward_probs,
                wear_reward,
                wear_reward_stimuli,
                wear_reward_probs,
            ) = draw_reward(
                r1,
                r2,
                r3,
                r4,
                t,
                block,
                number_of_trials_in_block,
                selected_person,
                stimuli_dict,
            )
            (
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
            ) = show_objects(stimuli_dict, fruit_reward_stimuli, wear_reward_stimuli)

            draw_first_choice_screen(
                window,
                wait_ch1,
                myclock,
                first_rectangle_loc,
                presented_person,
                stimuli_dict,
            )

            # wait for second keypress, returns a tuple with None if no response
            keych2 = choice(ch_deadline, myclock)
            # update data
            data_file_vars = update_data_ch2(data_file_vars, key1, rt1, selected_person)
            # abort trial if no response
            if keych2 == None:
                presented_person.autoDraw = False  # remove presented person
                too_slow_func(window, too_slow)
                save_data(data_file, data_file_vars)
                continue
            # check if wrong key or opposite key was pressed
            elif (
                (keych2[0][0] == "s" and first_object_loc != -3.0)
                or (keych2[0][0] == "k" and first_object_loc != 3.0)
                or (keych2[0][0] not in ("s", "k"))
            ):
                presented_person.autoDraw = False  # remove presented person
                wrong_key_func(window, wrong_key)
                save_data(data_file, data_file_vars)
                continue

            # get second keypress
            key2, rt2 = keych2[0]
            draw_second_choice_screen(
                window, wait_ch2, first_rectangle_loc, draw_first_object
            )
            stimuli_dict = draw_first_reward(
                window,
                stimuli_dict,
                first_reward,
                wait_outcome2,
                first_rectangle_loc,
                first_reward_position,
                draw_covers,
                second_rectangle_loc,
                myclock,
            )

            # wait for third keypress
            keych3 = choice(ch_deadline, myclock)
            # update data
            data_file_vars = update_data_ch3(
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
            )
            # no response
            if keych3 == None:
                presented_person.autoDraw = False  # remove presented person
                too_slow_func(window, too_slow)
                save_data(data_file, data_file_vars)
                continue
            # wrong key or opposite key
            elif (
                (keych3[0][0] == "s" and second_object_loc != -3.0)
                or (keych3[0][0] == "k" and second_object_loc != 3.0)
                or (keych3[0][0] not in ("s", "k"))
            ):
                presented_person.autoDraw = False  # remove presented person
                wrong_key_func(window, wrong_key)
                save_data(data_file, data_file_vars)
                continue
            key3, rt3 = keych3[0]
            stimuli_dict, presented_person = draw_second_object_and_reward(
                window,
                stimuli_dict,
                presented_person,
                wait_ch3,
                wait_outcome3,
                second_reward,
                second_reward_position,
                draw_second_stimulus,
                second_rectangle_loc,
            )
            # update full data
            data_file_vars = update_data_full(
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
            )
            save_data(data_file, data_file_vars)
    return data_file

