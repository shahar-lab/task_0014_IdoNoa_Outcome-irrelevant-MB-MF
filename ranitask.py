from numpy.random import choice
from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
import numpy as np

# get subject_num
expInfo = {"subject": "999"}
dlg = gui.DlgFromDict(expInfo, title="Two-armed bandit task")  # update expInfo
subject_num = int(expInfo["subject"])

# create a text file to save data
fileName = "rani_task" + expInfo["subject"] + "_" + data.getDateStr()
monitor_size = monitors.Monitor("testMonitor").getSizePix()
data_file = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'

data_file.write(
    "subject,block_type,block,trial, left_person,left_person_fruit,left_person_wear, right_person,right_person_fruit,right_person_wear, ch_person,ch_fruit,ch_wear,keypress1, rt1, exp_value_ch_fruit, reward_fruit, exp_value_ch_wear, reward_wear, keypress2, rt2, keypress3, rt3,first_product,second_product, fruit_location,exp_value_fruit1,exp_value_fruit2,wear_location,exp_value_wear1,exp_value_wear2,iti\n"
)
# create window display
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
fruit = [
    "images/f1.png",
    "images/f2.png",
    "images/f2.png",
    "images/f1.png",
]  # f1 is bannana, f2 is orange
wear = [
    "images/c1.png",
    "images/c2.png",
    "images/c1.png",
    "images/c2.png",
]  # c refers to clothing, c1 is hat, c2 is shirt.

# associating each person with its fruit and wear
model = np.array(
    [[fruit[0], wear[0]], [fruit[1], wear[1]], [fruit[2], wear[2]], [fruit[3], wear[3]]]
)
# only pairs of persons who share an object are valid, irrespictable of location
valid_pairs = np.array([[0, 2], [2, 0], [0, 3], [3, 0], [1, 2], [2, 1], [1, 3], [3, 1]])

# locations in pixels units referring to left or right locations of objects
left_right_locations = [
    3,
    -3,
]
# initiation
selected_person = None

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
if subject_num % 2 == 0:
    rwalk = np.genfromtxt("rndwalk/rndwalk2.csv", delimiter=",")
else:
    rwalk = np.genfromtxt("rndwalk/rndwalk1.csv", delimiter=",")
r1 = rwalk[0, :]
r2 = rwalk[1, :]
r3 = rwalk[2, :]
r4 = rwalk[3, :]

# defining the rectangle used to mark selection
def rect(x1, x2, y1, y2):
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


# This function runs a loop of trials
def mytrials(
    subject_num,  # the serial number of the subject
    block_type,  # whether it is a training block or a test block
    number_of_blocks,  # number of blocks
    number_of_trials_in_block,  # number of trials to run in every block
    iti,  # inter trial interval
    ch_deadline,  # choice deadline
    wait_ch1,  # waiting time after first choice
    wait_ch2,  # waiting time after second choice
    wait_ch3,  # waiting time after third choice
    wait_outcome2,  # waiting time after second outcome
    wait_outcome3,  # waiting time after third outcome
):

    # check keyboard presses
    kb = keyboard.Keyboard()
    kb.start()

    # for loop running on the number of blocks
    for block in range(number_of_blocks):

        # making pauses on every start of block which is not the first
        if block != 0:
            game_pause.draw()
            window.update()
            event.waitKeys(keyList=["space"])
        # for loop running on each trial
        for t in range(number_of_trials_in_block):
            # aborting the experiment if escape is pressed
            keys = kb.getKeys(["escape"])
            if "escape" in keys:
                window.close()
                core.quit()
            # get the current pair out of possible 8 pairs
            person_pair = valid_pairs[np.random.choice(8, 1)[0]]

            # draw randomly the locations of the fruit and of the wear
            fruit_loc_pxl = np.random.choice(left_right_locations)
            wear_loc_pxl = np.random.choice(left_right_locations)
            if fruit_loc_pxl == -3:  # this is the location on screen
                fruit_loc = "left"
            else:
                fruit_loc = "right"
            if wear_loc_pxl == -3:
                wear_loc = "left"
            else:
                wear_loc = "right"

            # counterbalance of stimulus presentation - fruit shown first or wear first.
            fruit_appear_first = np.random.choice(2)

            # define the stimuli according to the raffled pair
            left_person = visual.ImageStim(
                window, image=person_list[person_pair[0]], pos=[-6, 5], interpolate=True
            )
            right_person = visual.ImageStim(
                window, image=person_list[person_pair[1]], pos=[6, 5], interpolate=True
            )

            fruit_stimulus = visual.ImageStim(
                window, image=None, pos=[fruit_loc_pxl, 0], size=2
            )
            fruit_cover = visual.ImageStim(
                window, image="images/fruit_cvr.png", pos=[fruit_loc_pxl, 0]
            )
            wear_stimulus = visual.ImageStim(
                window, image=None, pos=[wear_loc_pxl, -5], size=2
            )
            wear_cover = visual.ImageStim(
                window, image="images/wear_cvr.png", pos=[wear_loc_pxl, -5]
            )

            fruit_green_base = visual.ImageStim(
                window, image="images/greenbase.png", pos=[-fruit_loc_pxl, -0.5]
            )
            wear_green_base = visual.ImageStim(
                window, image="images/greenbase.png", pos=[-wear_loc_pxl, -6]
            )

            # define won/lost feedback, some stimuli
            won = visual.ImageStim(
                window, image="images/rw.jpg", pos=[0, 0], size=2, interpolate=True
            )
            lost = visual.ImageStim(
                window, image="images/ur.jpg", pos=[0, 0], size=2, interpolate=True
            )

            # draw the stimuli and update the window
            window.flip(clearBuffer=True)
            fixation.draw()
            window.update()
            core.wait(iti)
            left_person.draw()
            right_person.draw()
            fruit_cover.draw()
            wear_cover.draw()
            fruit_green_base.draw()
            wear_green_base.draw()
            rect(-0.7, 0.7, 0.3, 0.7)
            window.update()
            myclock = core.Clock()

            # wait for person choice
            keysEvent = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)

            # if no response was pressed, show "Too Slow" and save current trial to csv
            if keysEvent == None:
                too_slow.draw()
                window.update()
                core.wait(1)
                data_file.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f change to R notation from python notation
                        t + 1,  # f
                        # choice
                        person_pair[0] + 1,  # f left_person
                        int(fruit[person_pair[0]][8]),  # f left_person_fruit
                        int(wear[person_pair[0]][8]),  # f left_person_wear
                        person_pair[1] + 1,  # f right_person
                        int(fruit[person_pair[1]][8]),  # f right_person_fruit
                        int(wear[person_pair[1]][8]),  # f right_person_wear
                        np.nan,  # f ch_person
                        np.nan,  # f ch_person_fruit
                        np.nan,  # f ch_person_wear
                        np.nan,  # s key1
                        np.nan,  # f rt1
                        # outcomes
                        np.nan,  # f  exp_value_ch_fruit
                        np.nan,  # f reward_fruit
                        np.nan,  # f exp_value_ch_wear
                        np.nan,  # f reward_ch_wear
                        np.nan,  # s key2
                        np.nan,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
                        np.nan,  # s first_product (fruit/wear)
                        np.nan,  # s second_product (fruit/wear)
                        np.nan,  # s fruit_loc
                        r1[t + block * number_of_trials_in_block],  # f exp_value_fruit1
                        r2[t + block * number_of_trials_in_block],  # f exp_value_fruit2
                        np.nan,  # s wear_loc
                        r3[t + block * number_of_trials_in_block],  # f exp_value_wear1
                        r4[t + block * number_of_trials_in_block],  # f exp_value_wear2
                        iti,  # f iti
                    )
                )
                continue

            # set the stimulus by the selected choice (left or right)
            key1, RT1 = keysEvent[0]
            if key1 == "s":
                selected_person = person_pair[0]
                unselectedPerson = person_pair[1]
                # the fruit and wear arrays are organized according to the model, thus choosing fruit[selected_person] gives the selected_person's fruit.
                fruit_stimulus.image = fruit[selected_person]
                wear_stimulus.image = wear[selected_person]
                presented_person = left_person
            elif key1 == "k":
                selected_person = person_pair[1]
                unselectedPerson = person_pair[0]
                fruit_stimulus.image = fruit[selected_person]
                wear_stimulus.image = wear[selected_person]
                presented_person = right_person

            # if space was pressed it means the participants wanted a break
            elif key1 == "space":
                data_file.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f +1 changes from 0 to 1
                        t + 1,  # f +1 changes from 0 to 1
                        # choice
                        person_pair[0] + 1,  # f left_person
                        int(fruit[person_pair[0]][8]),  # f left_person_fruit
                        int(wear[person_pair[0]][8]),  # f left_person_wear
                        person_pair[1] + 1,  # f right_person
                        int(fruit[person_pair[1]][8]),  # f right_person_fruit
                        int(wear[person_pair[1]][8]),  # f right_person_wear
                        np.nan,  # f ch_person
                        np.nan,  # f ch_person_fruit
                        np.nan,  # f ch_person_wear
                        np.nan,  # s key1
                        np.nan,  # f rt1
                        # outcomes
                        np.nan,  # f  exp_value_ch_fruit
                        np.nan,  # f reward_fruit
                        np.nan,  # f exp_value_ch_wear
                        np.nan,  # f reward_ch_wear
                        np.nan,  # s key2
                        np.nan,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
                        np.nan,  # s first_product (fruit/wear)
                        np.nan,  # s second_product (fruit/wear)
                        np.nan,  # s fruit_loc
                        r1[t + block * number_of_trials_in_block],  # f exp_value_fruit1
                        r2[t + block * number_of_trials_in_block],  # f exp_value_fruit2
                        np.nan,  # s wear_loc
                        r3[t + block * number_of_trials_in_block],  # f exp_value_wear1
                        r4[t + block * number_of_trials_in_block],  # f exp_value_wear2
                        iti,  # f iti
                    )
                )
                call_supervisor.draw()
                window.update()
                event.waitKeys(keyList=["space"])
                core.wait(2)
                continue

            # if another key was chosen it means a wrong key was pressed
            else:
                wrong_key.draw()
                window.update()
                core.wait(1)
                data_file.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f +1 - changes from 0 to 1
                        t + 1,  # f +1 - changes from 0 to 1
                        # choice
                        person_pair[0] + 1,  # f left_person
                        int(fruit[person_pair[0]][8]),  # f left_person_fruit
                        int(wear[person_pair[0]][8]),  # f left_person_wear
                        person_pair[1] + 1,  # f right_person
                        int(fruit[person_pair[1]][8]),  # f right_person_fruit
                        int(wear[person_pair[1]][8]),  # f right_person_wear
                        np.nan,  # f ch_person
                        np.nan,  # f ch_person_fruit
                        np.nan,  # f ch_person_wear
                        np.nan,  # s key1
                        np.nan,  # f rt1
                        # outcomes
                        np.nan,  # f  exp_value_ch_fruit
                        np.nan,  # f reward_fruit
                        np.nan,  # f exp_value_ch_wear
                        np.nan,  # f reward_ch_wear
                        np.nan,  # s key2
                        np.nan,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
                        np.nan,  # s first_product (fruit/wear)
                        np.nan,  # s second_product (fruit/wear)
                        np.nan,  # s fruit_loc
                        r1[t + block * number_of_trials_in_block],  # f exp_value_fruit1
                        r2[t + block * number_of_trials_in_block],  # f exp_value_fruit2
                        np.nan,  # s wear_loc
                        r3[t + block * number_of_trials_in_block],  # f exp_value_wear1
                        r4[t + block * number_of_trials_in_block],  # f exp_value_wear2
                        iti,  # f iti
                    )
                )
                continue
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
                fruit_reward_stimuli = won
            else:
                fruit_reward = 0
                fruit_reward_stimuli = lost
            if np.random.random() < wear_reward_probs[selected_person]:
                wear_reward = 1
                wear_reward_stimuli = won
            else:
                wear_reward = 0
                wear_reward_stimuli = lost

            # draw according to counterbalanced order of object appearance
            if fruit_appear_first:
                first_rectangle_loc = (-0.7, 0.7, -0.24, 0.26)
                second_rectangle_loc = (-0.7, 0.7, -0.78, -0.24)
                draw_first_object = (fruit_stimulus, wear_cover)
                draw_covers = (fruit_cover, wear_cover)
                draw_second_stimulus = (fruit_cover, wear_stimulus)
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
                draw_first_object = (fruit_cover, wear_stimulus)
                draw_covers = (fruit_cover, wear_cover)
                draw_second_stimulus = (fruit_stimulus, wear_cover)
                first_reward = wear_reward_stimuli
                second_reward = fruit_reward_stimuli
                first_reward_position = -5
                second_reward_position = 0
                first_object_loc = wear_stimulus.pos[0]
                second_object_loc = fruit_stimulus.pos[0]
                first_product = "wear"
                second_product = "fruit"

            # drawing the stimuli
            presented_person.autoDraw = True
            fruit_cover.draw()
            wear_cover.draw()
            rect(-0.7, 0.7, 0.3, 0.7)
            window.flip()
            core.wait(wait_ch1)
            fruit_cover.draw()
            wear_cover.draw()
            rect(*first_rectangle_loc)
            window.callOnFlip(myclock.reset)
            window.flip()

            # wait for second keypress
            keych2 = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)
            # abort trial if no response
            if keych2 == None:
                presented_person.autoDraw = False
                too_slow.draw()
                window.update()
                core.wait(1)
                # write the trial data and continue to the next trial
                data_file.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f +1 - changes from 0 to 1
                        t + 1,  # f +1 - changes from 0 to 1
                        # choice
                        person_pair[0] + 1,  # f left_person
                        int(fruit[person_pair[0]][8]),  # f left_person_fruit
                        int(wear[person_pair[0]][8]),  # f left_person_wear
                        person_pair[1] + 1,  # f right_person
                        int(fruit[person_pair[1]][8]),  # f right_person_fruit
                        int(wear[person_pair[1]][8]),  # f right_person_wear
                        selected_person + 1,  # f ch_person
                        int(fruit[selected_person][8]),  # f ch_person_fruit
                        int(wear[selected_person][8]),  # f ch_person_wear
                        key1,  # s key1
                        RT1 * 1000,  # f rt1
                        # outcomes
                        np.nan,  # f  exp_value_ch_fruit
                        np.nan,  # f reward_fruit
                        np.nan,  # f exp_value_ch_wear
                        np.nan,  # f reward_ch_wear
                        np.nan,  # s key2
                        np.nan,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
                        np.nan,  # s first_product (fruit/wear)
                        np.nan,  # s second_product (fruit/wear)
                        np.nan,  # s fruit_loc
                        r1[t + block * number_of_trials_in_block],  # f exp_value_fruit1
                        r2[t + block * number_of_trials_in_block],  # f exp_value_fruit2
                        np.nan,  # s wear_loc
                        r3[t + block * number_of_trials_in_block],  # f exp_value_wear1
                        r4[t + block * number_of_trials_in_block],  # f exp_value_wear2
                        iti,  # f iti
                    )
                )
                continue
            # check if wrong key or opposite key
            elif (
                (keych2[0][0] == "s" and first_object_loc != -3.0)
                or (keych2[0][0] == "k" and first_object_loc != 3.0)
                or (keych2[0][0] not in ("s", "k"))
            ):
                presented_person.autoDraw = False
                wrong_key.draw()
                window.update()
                core.wait(1)
                data_file.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f +1 - changes from 0 to 1
                        t + 1,  # f +1 - changes from 0 to 1
                        # choice
                        person_pair[0] + 1,  # f left_person
                        int(fruit[person_pair[0]][8]),  # f left_person_fruit
                        int(wear[person_pair[0]][8]),  # f left_person_wear
                        person_pair[1] + 1,  # f right_person
                        int(fruit[person_pair[1]][8]),  # f right_person_fruit
                        int(wear[person_pair[1]][8]),  # f right_person_wear
                        selected_person + 1,  # f ch_person
                        int(fruit[selected_person][8]),  # f ch_person_fruit
                        int(wear[selected_person][8]),  # f ch_person_wear
                        key1,  # s key1
                        RT1 * 1000,  # f rt1
                        # outcomes
                        np.nan,  # f  exp_value_ch_fruit
                        np.nan,  # f reward_fruit
                        np.nan,  # f exp_value_ch_wear
                        np.nan,  # f reward_ch_wear
                        np.nan,  # s key2
                        np.nan,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
                        np.nan,  # s first_product (fruit/wear)
                        np.nan,  # s second_product (fruit/wear)
                        np.nan,  # s fruit_loc
                        r1[t + block * number_of_trials_in_block],  # f exp_value_fruit1
                        r2[t + block * number_of_trials_in_block],  # f exp_value_fruit2
                        np.nan,  # s wear_loc
                        r3[t + block * number_of_trials_in_block],  # f exp_value_wear1
                        r4[t + block * number_of_trials_in_block],  # f exp_value_wear2
                        iti,  # f iti
                    )
                )
                continue
            key2, RT2 = keych2[0]

            # draw first object
            draws(*draw_first_object)
            rect(*first_rectangle_loc)
            window.flip()
            core.wait(wait_ch2)
            draws(*draw_first_object)
            # defining the location of the reward
            won.pos = [0, first_reward_position]
            lost.pos = [0, first_reward_position]
            first_reward.draw()
            rect(*first_rectangle_loc)
            window.flip()
            core.wait(wait_outcome2)
            # d3
            draws(*draw_covers)
            rect(*second_rectangle_loc)
            window.callOnFlip(myclock.reset)
            window.flip()

            # wait for third keypress
            keych3 = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)

            # no response
            if keych3 == None:
                # fill with nans the reward related variables of the second choice object
                if fruit_appear_first:
                    wear_reward_probs = [np.nan, np.nan, np.nan, np.nan]
                    wear_reward = np.nan
                else:
                    fruit_reward_probs = [np.nan, np.nan, np.nan, np.nan]
                    fruit_reward = np.nan
                presented_person.autoDraw = False
                too_slow.draw()
                window.update()
                core.wait(1)
                data_file.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%f,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f +1 - changes from 0 to 1
                        t + 1,  # f +1 - changes from 0 to 1
                        # choice
                        person_pair[0] + 1,  # f left_person
                        int(fruit[person_pair[0]][8]),  # f left_person_fruit
                        int(wear[person_pair[0]][8]),  # f left_person_wear
                        person_pair[1] + 1,  # f right_person
                        int(fruit[person_pair[1]][8]),  # f right_person_fruit
                        int(wear[person_pair[1]][8]),  # f right_person_wear
                        selected_person + 1,  # f ch_person
                        int(fruit[selected_person][8]),  # f ch_person_fruit
                        int(wear[selected_person][8]),  # f ch_person_wear
                        key1,  # s key1
                        RT1 * 1000,  # f rt1
                        # outcomes
                        fruit_reward_probs[selected_person],  # f  exp_value_ch_fruit
                        fruit_reward,  # f reward_fruit
                        wear_reward_probs[selected_person],  # f exp_value_ch_wear
                        wear_reward,  # f reward_ch_wear
                        key2,  # s key2
                        RT2 * 1000,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
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
                continue
            # wrong key or opposite key
            elif (
                (keych3[0][0] == "s" and second_object_loc != -3.0)
                or (keych3[0][0] == "k" and second_object_loc != 3.0)
                or (keych3[0][0] not in ("s", "k"))
            ):
                presented_person.autoDraw = False
                wrong_key.draw()
                window.update()
                core.wait(1)
                if fruit_appear_first == ["FruitFirst"]:
                    wear_reward_probs = [np.nan, np.nan, np.nan, np.nan]
                    wear_reward = np.nan
                else:
                    fruit_reward_probs = [np.nan, np.nan, np.nan, np.nan]
                    fruit_reward = np.nan
                    data_file.write(
                        "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%f,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
                        % (
                            # general
                            subject_num,  # f
                            block_type,  # s
                            block + 1,  # f +1 - changes from 0 to 1
                            t + 1,  # f +1 - changes from 0 to 1
                            # choice
                            person_pair[0] + 1,  # f left_person
                            int(fruit[person_pair[0]][8]),  # f left_person_fruit
                            int(wear[person_pair[0]][8]),  # f left_person_wear
                            person_pair[1] + 1,  # f right_person
                            int(fruit[person_pair[1]][8]),  # f right_person_fruit
                            int(wear[person_pair[1]][8]),  # f right_person_wear
                            selected_person + 1,  # f ch_person
                            int(fruit[selected_person][8]),  # f ch_person_fruit
                            int(wear[selected_person][8]),  # f ch_person_wear
                            key1,  # s key1
                            RT1 * 1000,  # f rt1
                            # outcomes
                            fruit_reward_probs[
                                selected_person
                            ],  # f  exp_value_ch_fruit
                            fruit_reward,  # f reward_fruit
                            wear_reward_probs[selected_person],  # f exp_value_ch_wear
                            wear_reward,  # f reward_ch_wear
                            key2,  # s key2
                            RT2 * 1000,  # f rt2
                            np.nan,  # f key3
                            np.nan,  # f rt3
                            first_product,  # s first_product (fruit/wear)
                            second_product,  # s second_product (fruit/wear)
                            fruit_loc,  # s fruit_loc
                            r1[
                                t + block * number_of_trials_in_block
                            ],  # f exp_value_fruit1
                            r2[
                                t + block * number_of_trials_in_block
                            ],  # f exp_value_fruit2
                            wear_loc,  # s wear_loc
                            r3[
                                t + block * number_of_trials_in_block
                            ],  # f exp_value_wear1
                            r4[
                                t + block * number_of_trials_in_block
                            ],  # f exp_value_wear2
                            iti,  # f iti
                        )
                    )
                continue
            key3, RT3 = keych3[0]
            draws(*draw_second_stimulus)
            rect(*second_rectangle_loc)
            window.flip()
            core.wait(wait_ch3)
            won.pos = [0, second_reward_position]
            lost.pos = [0, second_reward_position]
            draws(*draw_second_stimulus)
            second_reward.draw()
            rect(*second_rectangle_loc)
            window.flip()
            core.wait(wait_outcome3)
            draws(*draw_second_stimulus)
            window.flip()
            presented_person.autoDraw = False

            # full print
            data_file.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%s,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f subject
                    block_type,  # s block_type
                    block + 1,  # f block_num : +1 - changes from 0 to 1
                    t + 1,  # trial_num f +1 - changes from 0 to 1
                    # choice
                    person_pair[0] + 1,  # f left_person
                    int(fruit[person_pair[0]][8]),  # f left_person_fruit
                    int(wear[person_pair[0]][8]),  # f left_person_wear
                    person_pair[1] + 1,  # f right_person
                    int(fruit[person_pair[1]][8]),  # f right_person_fruit
                    int(wear[person_pair[1]][8]),  # f right_person_wear
                    selected_person + 1,  # f ch_person
                    int(fruit[selected_person][8]),  # f ch_person_fruit
                    int(wear[selected_person][8]),  # f ch_person_wear
                    key1,  # s key1
                    RT1 * 1000,  # f rt1
                    # outcomes
                    fruit_reward_probs[selected_person],  # f  exp_value_ch_fruit
                    fruit_reward,  # f reward_fruit
                    wear_reward_probs[selected_person],  # f exp_value_ch_wear
                    wear_reward,  # f reward_ch_wear
                    key2,  # s key2
                    RT2 * 1000,  # f rt2
                    key3,  # s key3
                    RT3 * 1000,  # f rt3
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
    return


# This is the timeline including the instructions, quiz, training and test parts.

# instructions
num_instructions = 14
for instruction in range(1, num_instructions + 1):
    test_instructions = visual.ImageStim(
        window,
        image="instructions/instructions_test/Test" + str(instruction) + ".png",
        pos=[0, 0],
        interpolate=True,
    )
    test_instructions.draw()
    window.update()
    event.waitKeys(keyList=["space", "s", "k"])

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
quiz1 = visual.ImageStim(
    window, image="instructions/quiz/quiz1" + ".png", pos=[0, 0], interpolate=True,
)
quiz1.draw()
window.update()
event.waitKeys(keyList=["s"])

quiz2 = visual.ImageStim(
    window, image="instructions/quiz/quiz2" + ".png", pos=[0, 0], interpolate=True,
)
quiz2.draw()
window.update()
event.waitKeys(keyList=["s"])
quiz3 = visual.ImageStim(
    window, image="instructions/quiz/quiz3" + ".png", pos=[0, 0], interpolate=True,
)
quiz3.draw()
window.update()
event.waitKeys(keyList=["k"])
quiz4 = visual.ImageStim(
    window, image="instructions/quiz/quiz4" + ".png", pos=[0, 0], interpolate=True,
)
quiz4.draw()
window.update()
event.waitKeys(keyList=["s"])

quiz5 = visual.ImageStim(
    window, image="instructions/quiz/quiz5" + ".png", pos=[0, 0], interpolate=True,
)
quiz5.draw()
window.update()
event.waitKeys(keyList=["k"])

# training
start_training = visual.ImageStim(
    window,
    image="instructions/instructions_test/start_training.png",
    pos=[0, 0],
    interpolate=True,
)
start_training.draw()
window.update()
event.waitKeys(keyList=["space"])

mytrials(
    subject_num=subject_num,
    block_type="train",
    number_of_blocks=1,
    number_of_trials_in_block=10,
    iti=1,
    ch_deadline=6,
    wait_ch1=0.5,
    wait_ch2=0.5,
    wait_ch3=0.5,
    wait_outcome2=1,
    wait_outcome3=1,
)
start_test = visual.ImageStim(
    window,
    image="instructions/instructions_test/start_test.png",
    pos=[0, 0],
    interpolate=True,
)

# test
start_test.draw()
window.update()
event.waitKeys(keyList=["space"])
mytrials(
    subject_num=subject_num,
    block_type="test",
    number_of_blocks=5,
    number_of_trials_in_block=40,
    iti=1,
    ch_deadline=6,
    wait_ch1=0.5,
    wait_ch2=0.5,
    wait_ch3=0.5,
    wait_outcome2=1,
    wait_outcome3=1,
)
finish_test = visual.ImageStim(
    window,
    image="instructions/instructions_test/finish_test.png",
    pos=[0, 0],
    interpolate=True,
)
finish_test.draw()
window.update()
event.waitKeys(keyList=["space"])
