from numpy.random import choice
from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
import numpy as np

# create a text file to save data
expInfo = {"subject": "999"}
dlg = gui.DlgFromDict(expInfo, title="Two-armed bandit task")
fileName = "ranitask" + expInfo["subject"] + "_" + data.getDateStr()
subject_num = int(expInfo["subject"])
monitor_size = monitors.Monitor("testMonitor").getSizePix()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write(
    "subject,block_type,block,trial, left_person,left_person_fruit,left_person_wear, right_person,right_person_fruit,right_person_wear, ch_person,ch_fruit,ch_wear,keypress1, rt1, exp_value_ch_fruit, reward_fruit, exp_value_ch_wear, reward_wear, keypress2, rt2, keypress3, rt3,first_product,second_product, fruit_location,exp_value_fruit1,exp_value_fruit2,wear_location,exp_value_wear1,exp_value_wear2,iti\n"
)
win = visual.Window(
    monitor="testMonitor",
    screen=0,
    units="deg",
    color=(255, 255, 255),
    fullscr=True,
    allowStencil=True,
)
win.mouseVisible = False
# ser = serial.Serial("COM3", 9600)


humansLst = ["m1.png", "m2.png", "w1.png", "w2.png"]
fruit = ["f1.png", "f2.png", "f2.png", "f1.png"]
wear = ["c1.png", "c2.png", "c1.png", "c2.png"]
model = np.array(
    [[fruit[0], wear[0]], [fruit[1], wear[1]], [fruit[2], wear[2]], [fruit[3], wear[3]]]
)
# only pairs who share an object are valid
valid_pairs = np.array([[0, 2], [2, 0], [0, 3], [3, 0], [1, 2], [2, 1], [1, 3], [3, 1]])
cond = [3, 6]
rndsmple = [3, -3]
selected_person = None
fixation = visual.TextStim(win, text="+", pos=[0, 0], color=(0, 0, 0))
Tooslow = visual.TextStim(win, text="Too Slow", pos=[0, 0], color=(0, 0, 0))
wrongkey = visual.TextStim(win, text="Wrong Key", pos=[0, 0], color=(0, 0, 0))
call = visual.TextStim(win, text="call supervisor", pos=[0, 0], color=(0, 0, 0))
game_pause = visual.ImageStim(
    win,
    image="instructions/instructions_test/game_pause.png",
    pos=[0, 0],
    interpolate=True,
)
# get counterbalanced randomwalk
if subject_num % 2 == 0:
    rwalk = np.genfromtxt("rndwalk/rndwalk1.csv", delimiter=",")
else:
    rwalk = np.genfromtxt("rndwalk/rndwalk2.csv", delimiter=",")
r1 = rwalk[0, :]
r2 = rwalk[1, :]
r3 = rwalk[2, :]
r4 = rwalk[3, :]
print(r1)

keych2 = 0


def rect(x1, x2, y1, y2):
    a = visual.Line(win, start=(x1, y1), end=(x2, y1), size=10, lineColor=[1.0, -1, -1])
    b = visual.Line(win, start=(x1, y1), end=(x1, y2), size=10, lineColor=[1.0, -1, -1])
    c = visual.Line(win, start=(x2, y2), end=(x2, y1), size=10, lineColor=[1.0, -1, -1])
    d = visual.Line(win, start=(x2, y2), end=(x1, y2), size=10, lineColor=[1.0, -1, -1])
    a.draw()
    b.draw()
    c.draw()
    d.draw()
    return


def draws(one, two):
    one.draw()
    two.draw()
    return


# defining a single trial
def mytrials(
    subject_num,
    block_type,
    Ntrls,
    iti,
    ch_deadline,
    fdbck_ch1,
    fdbck_ch2,
    fdbck_ch3,
    outcome_ch2,
    outcome_ch3,
):

    # check keyboard presses
    kb = keyboard.Keyboard()
    kb.start()
    trials_in_block = 5
    block = 0
    for t in range(Ntrls):
        if t % trials_in_block == 0 & t != Ntrls - 1 & t != 0:
            block += 1  # update block number
            game_pause.draw()
            win.update()
            event.waitKeys(keyList=["space"])
        keys = kb.getKeys(["escape"])
        if "escape" in keys:
            win.close()
            core.quit()
        sampled_stim_idx = np.random.choice(8, 1)  # get a pair index
        sampled_stim = valid_pairs[sampled_stim_idx[0]]  # get the pair values
        rndlocation = np.random.choice(rndsmple, 2)
        if rndlocation[0] == -3:  # this is the location on screen
            fruit_loc = "left"
        else:
            fruit_loc = "right"
        if rndlocation[1] == -3:
            wear_loc = "left"
        else:
            wear_loc = "right"
        # define the stimuli
        LStim = visual.ImageStim(
            win, image=humansLst[sampled_stim[0]], pos=[-6, 5], interpolate=True
        )
        RStim = visual.ImageStim(
            win, image=humansLst[sampled_stim[1]], pos=[6, 5], interpolate=True
        )
        FruitStim = visual.ImageStim(
            win, image=fruit[0], pos=[rndlocation[0], 0], size=2
        )
        WearStim = visual.ImageStim(
            win, image=wear[0], pos=[rndlocation[1], -5], size=2
        )
        FruitCvr = visual.ImageStim(win, image="fruit.png", pos=[rndlocation[0], 0])
        WearCvr = visual.ImageStim(win, image="clothing.png", pos=[rndlocation[1], -5])
        GreenBase = visual.ImageStim(
            win, image="greenbase.png", pos=[-rndlocation[1], -6]
        )
        GreenBase1 = visual.ImageStim(
            win, image="greenbase.png", pos=[-rndlocation[0], -0.5]
        )

        # define won/lost feedback, some stimuli
        won = visual.ImageStim(
            win, image="rw.jpg", pos=[0, 0], size=2, interpolate=True
        )
        lost = visual.ImageStim(
            win, image="ur.jpg", pos=[0, 0], size=2, interpolate=True
        )

        # draw the stimuli and update the window
        win.flip(clearBuffer=True)
        fixation.draw()
        win.update()
        core.wait(iti)
        LStim.draw()
        RStim.draw()
        FruitCvr.draw()
        WearCvr.draw()
        GreenBase.draw()
        GreenBase1.draw()
        rect(-0.7, 0.7, 0.3, 0.7)
        win.update()
        myclock = core.Clock()

        # wait for keypress
        keysEvent = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)
        if keysEvent == None:
            Tooslow.draw()
            win.update()
            core.wait(1)
            dataFile.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f
                    block_type,  # s
                    block + 1,  # f +1 - changes from 0 to 1
                    t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                    # choice
                    sampled_stim[0] + 1,  # f left_person
                    int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                    int(wear[sampled_stim[0]][1]),  # f left_person_wear
                    sampled_stim[1] + 1,  # f right_person
                    int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                    int(wear[sampled_stim[1]][1]),  # f right_person_wear
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
                    r1[t],  # f exp_value_fruit1
                    r2[t],  # f exp_value_fruit2
                    np.nan,  # s wear_loc
                    r3[t],  # f exp_value_wear1
                    r4[t],  # f exp_value_wear2
                    iti,  # f iti
                )
            )
            continue
        keys, RT1 = keysEvent[0]

        # set the variables by the selected choice (left or right)
        if keys == "s":
            selected_person = sampled_stim[0]
            UnselectedPerson = sampled_stim[1]
            FruitStim.image = fruit[selected_person]
            WearStim.image = wear[selected_person]
            PresentedStim = LStim
        elif keys == "k":
            selected_person = sampled_stim[1]
            UnselectedPerson = sampled_stim[0]
            FruitStim.image = fruit[selected_person]
            WearStim.image = wear[selected_person]
            PresentedStim = RStim
        elif keys == "space":
            dataFile.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f
                    block_type,  # s
                    block + 1,  # f +1 - changes from 0 to 1
                    t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                    # choice
                    sampled_stim[0] + 1,  # f left_person
                    int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                    int(wear[sampled_stim[0]][1]),  # f left_person_wear
                    sampled_stim[1] + 1,  # f right_person
                    int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                    int(wear[sampled_stim[1]][1]),  # f right_person_wear
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
                    r1[t],  # f exp_value_fruit1
                    r2[t],  # f exp_value_fruit2
                    np.nan,  # s wear_loc
                    r3[t],  # f exp_value_wear1
                    r4[t],  # f exp_value_wear2
                    iti,  # f iti
                )
            )
            call.draw()
            win.update()
            event.waitKeys(keyList=["space"])
            core.wait(2)
            continue
        else:
            wrongkey.draw()
            win.update()
            core.wait(1)
            dataFile.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f
                    block_type,  # s
                    block + 1,  # f +1 - changes from 0 to 1
                    t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                    # choice
                    sampled_stim[0] + 1,  # f left_person
                    int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                    int(wear[sampled_stim[0]][1]),  # f left_person_wear
                    sampled_stim[1] + 1,  # f right_person
                    int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                    int(wear[sampled_stim[1]][1]),  # f right_person_wear
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
                    r1[t],  # f exp_value_fruit1
                    r2[t],  # f exp_value_fruit2
                    np.nan,  # s wear_loc
                    r3[t],  # f exp_value_wear1
                    r4[t],  # f exp_value_wear2
                    iti,  # f iti
                )
            )
            continue
        trialStims = (FruitStim.image + WearStim.image).replace(".png", "")
        ProbsFruit = [
            r1[t],
            r2[t],
            r2[t],
            r1[t],
        ]  # t starts from 1, and the python file from 0.
        ProbsWear = [r3[t], r4[t], r3[t], r4[t]]
        print(trialStims)
        print(ProbsFruit[selected_person])
        print(ProbsWear[selected_person])
        # check if won/lost by predetermined probablity of selected_person
        if np.random.random() < ProbsFruit[selected_person]:
            RewardFruit = won
            ResultFruit = 1
        else:
            RewardFruit = lost
            ResultFruit = 0
        if np.random.random() < ProbsWear[selected_person]:
            RewardWear = won
            ResultWear = 1
        else:
            RewardWear = lost
            ResultWear = 0

        # Counterbalance of stim presentation - Fruit first or Clothing first.
        topFirst = np.random.choice(("FruitFirst", "WearFirst"), 1)
        if topFirst == "FruitFirst":
            FirstRecDraw = (-0.7, 0.7, -0.24, 0.26)
            SecRecDraw = (-0.7, 0.7, -0.78, -0.24)
            Draw12 = (FruitStim, WearCvr)
            Draw3 = (FruitCvr, WearCvr)
            Draw456 = (FruitCvr, WearStim)
            Reward1 = RewardFruit
            Reward2 = RewardWear
            Rpos1 = 0
            Rpos2 = -5
            FrstLocation = FruitStim.pos[0]
            ScndLocation = WearStim.pos[0]
            first_product = "fruit"
            second_product = "wear"

        else:
            FirstRecDraw = (-0.7, 0.7, -0.78, -0.24)
            SecRecDraw = (-0.7, 0.7, -0.24, 0.26)
            Draw12 = (FruitCvr, WearStim)
            Draw3 = (FruitCvr, WearCvr)
            Draw456 = (FruitStim, WearCvr)
            Reward1 = RewardWear
            Reward2 = RewardFruit
            Rpos1 = -5
            Rpos2 = 0
            FrstLocation = WearStim.pos[0]
            ScndLocation = FruitStim.pos[0]
            first_product = "wear"
            second_product = "fruit"

        # the task itself, drawing the stimuli and the feedbacks
        PresentedStim.autoDraw = True
        FruitCvr.draw()
        WearCvr.draw()
        rect(-0.7, 0.7, 0.3, 0.7)
        win.flip()
        core.wait(fdbck_ch1)
        FruitCvr.draw()
        WearCvr.draw()
        rect(*FirstRecDraw)
        win.callOnFlip(myclock.reset)
        win.flip()
        keych2 = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)
        if keych2 == None:  # no response
            PresentedStim.autoDraw = False
            Tooslow.draw()
            win.update()
            core.wait(1)
            # write the trial data and continue to next trial
            dataFile.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f
                    block_type,  # s
                    block + 1,  # f +1 - changes from 0 to 1
                    t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                    # choice
                    sampled_stim[0] + 1,  # f left_person
                    int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                    int(wear[sampled_stim[0]][1]),  # f left_person_wear
                    sampled_stim[1] + 1,  # f right_person
                    int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                    int(wear[sampled_stim[1]][1]),  # f right_person_wear
                    selected_person + 1,  # f ch_person
                    int(fruit[selected_person][1]),  # f ch_person_fruit
                    int(wear[selected_person][1]),  # f ch_person_wear
                    keys,  # s key1
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
                    r1[t],  # f exp_value_fruit1
                    r2[t],  # f exp_value_fruit2
                    np.nan,  # s wear_loc
                    r3[t],  # f exp_value_wear1
                    r4[t],  # f exp_value_wear2
                    iti,  # f iti
                )
            )
            continue
        elif (
            (keych2[0][0] == "s" and FrstLocation != -3.0)
            or (keych2[0][0] == "k" and FrstLocation != 3.0)
            or (keych2[0][0] not in ("s", "k"))
        ):  # wrong key or opposite key
            PresentedStim.autoDraw = False
            wrongkey.draw()
            win.update()
            core.wait(1)
            dataFile.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%f,%f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f
                    block_type,  # s
                    block + 1,  # f +1 - changes from 0 to 1
                    t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                    # choice
                    sampled_stim[0] + 1,  # f left_person
                    int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                    int(wear[sampled_stim[0]][1]),  # f left_person_wear
                    sampled_stim[1] + 1,  # f right_person
                    int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                    int(wear[sampled_stim[1]][1]),  # f right_person_wear
                    selected_person + 1,  # f ch_person
                    int(fruit[selected_person][1]),  # f ch_person_fruit
                    int(wear[selected_person][1]),  # f ch_person_wear
                    keys,  # s key1
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
                    r1[t],  # f exp_value_fruit1
                    r2[t],  # f exp_value_fruit2
                    np.nan,  # s wear_loc
                    r3[t],  # f exp_value_wear1
                    r4[t],  # f exp_value_wear2
                    iti,  # f iti
                )
            )
            continue
        key2, RT2 = keych2[0]
        # print(keych2)
        # d1
        draws(*Draw12)
        rect(*FirstRecDraw)
        win.flip()
        core.wait(fdbck_ch2)
        # d2
        draws(*Draw12)
        won.pos = [0, Rpos1]
        lost.pos = [0, Rpos1]
        Reward1.draw()
        rect(*FirstRecDraw)
        win.flip()
        core.wait(outcome_ch2)
        # d3
        draws(*Draw3)
        rect(*SecRecDraw)
        win.callOnFlip(myclock.reset)
        win.flip()
        keych3 = event.waitKeys(maxWait=ch_deadline, timeStamped=myclock)
        if keych3 == None:  # no response
            if topFirst == ["FruitFirst"]:
                ProbsWear = [np.nan, np.nan, np.nan, np.nan]
                ResultWear = np.nan
            else:
                ProbsFruit = [np.nan, np.nan, np.nan, np.nan]
                ResultFruit = np.nan
            PresentedStim.autoDraw = False
            Tooslow.draw()
            win.update()
            core.wait(1)
            dataFile.write(
                "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%f,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
                % (
                    # general
                    subject_num,  # f
                    block_type,  # s
                    block + 1,  # f +1 - changes from 0 to 1
                    t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                    # choice
                    sampled_stim[0] + 1,  # f left_person
                    int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                    int(wear[sampled_stim[0]][1]),  # f left_person_wear
                    sampled_stim[1] + 1,  # f right_person
                    int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                    int(wear[sampled_stim[1]][1]),  # f right_person_wear
                    selected_person + 1,  # f ch_person
                    int(fruit[selected_person][1]),  # f ch_person_fruit
                    int(wear[selected_person][1]),  # f ch_person_wear
                    keys,  # s key1
                    RT1 * 1000,  # f rt1
                    # outcomes
                    ProbsFruit[selected_person],  # f  exp_value_ch_fruit
                    ResultFruit,  # f reward_fruit
                    ProbsWear[selected_person],  # f exp_value_ch_wear
                    ResultWear,  # f reward_ch_wear
                    key2,  # s key2
                    RT2 * 1000,  # f rt2
                    np.nan,  # f key3
                    np.nan,  # f rt3
                    first_product,  # s first_product (fruit/wear)
                    second_product,  # s second_product (fruit/wear)
                    fruit_loc,  # s fruit_loc
                    r1[t],  # f exp_value_fruit1
                    r2[t],  # f exp_value_fruit2
                    wear_loc,  # s wear_loc
                    r3[t],  # f exp_value_wear1
                    r4[t],  # f exp_value_wear2
                    iti,  # f iti
                )
            )
            continue
        elif (
            (keych3[0][0] == "s" and ScndLocation != -3.0)
            or (keych3[0][0] == "k" and ScndLocation != 3.0)
            or (keych3[0][0] not in ("s", "k"))
        ):  # wrong key or opposite key
            PresentedStim.autoDraw = False
            wrongkey.draw()
            win.update()
            core.wait(1)
            if topFirst == ["FruitFirst"]:
                ProbsWear = [np.nan, np.nan, np.nan, np.nan]
                ResultWear = np.nan
            else:
                ProbsFruit = [np.nan, np.nan, np.nan, np.nan]
                ResultFruit = np.nan
                dataFile.write(
                    "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%f,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
                    % (
                        # general
                        subject_num,  # f
                        block_type,  # s
                        block + 1,  # f +1 - changes from 0 to 1
                        t - trials_in_block * (block) + 1,  # f +1 - changes from 0 to 1
                        # choice
                        sampled_stim[0] + 1,  # f left_person
                        int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                        int(wear[sampled_stim[0]][1]),  # f left_person_wear
                        sampled_stim[1] + 1,  # f right_person
                        int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                        int(wear[sampled_stim[1]][1]),  # f right_person_wear
                        selected_person + 1,  # f ch_person
                        int(fruit[selected_person][1]),  # f ch_person_fruit
                        int(wear[selected_person][1]),  # f ch_person_wear
                        keys,  # s key1
                        RT1 * 1000,  # f rt1
                        # outcomes
                        ProbsFruit[selected_person],  # f  exp_value_ch_fruit
                        ResultFruit,  # f reward_fruit
                        ProbsWear[selected_person],  # f exp_value_ch_wear
                        ResultWear,  # f reward_ch_wear
                        key2,  # s key2
                        RT2 * 1000,  # f rt2
                        np.nan,  # f key3
                        np.nan,  # f rt3
                        first_product,  # s first_product (fruit/wear)
                        second_product,  # s second_product (fruit/wear)
                        fruit_loc,  # s fruit_loc
                        r1[t],  # f exp_value_fruit1
                        r2[t],  # f exp_value_fruit2
                        wear_loc,  # s wear_loc
                        r3[t],  # f exp_value_wear1
                        r4[t],  # f exp_value_wear2
                        iti,  # f iti
                    )
                )
            continue
        key3, RT3 = keych3[0]
        # d456
        draws(*Draw456)
        rect(*SecRecDraw)
        win.flip()
        core.wait(fdbck_ch3)
        won.pos = [0, Rpos2]
        lost.pos = [0, Rpos2]
        draws(*Draw456)
        Reward2.draw()
        rect(*SecRecDraw)
        win.flip()
        core.wait(outcome_ch3)
        draws(*Draw456)
        win.flip()
        PresentedStim.autoDraw = False

        dataFile.write(
            "%f,%s,%f,%f, %f,%f,%f ,%f,%f,%f ,%f,%f,%f ,%s,%f ,%f,%f,%f,%f ,%s,%f,%s,%f ,%s,%s,%s ,%f,%f,%s ,%f,%f,%f\n"
            % (
                # general
                subject_num,  # f subject
                block_type,  # s block_type
                block + 1,  # f block_num : +1 - changes from 0 to 1
                t
                - trials_in_block * (block)
                + 1,  # trial_num f +1 - changes from 0 to 1
                # choice
                sampled_stim[0] + 1,  # f left_person
                int(fruit[sampled_stim[0]][1]),  # f left_person_fruit
                int(wear[sampled_stim[0]][1]),  # f left_person_wear
                sampled_stim[1] + 1,  # f right_person
                int(fruit[sampled_stim[1]][1]),  # f right_person_fruit
                int(wear[sampled_stim[1]][1]),  # f right_person_wear
                selected_person + 1,  # f ch_person
                int(fruit[selected_person][1]),  # f ch_person_fruit
                int(wear[selected_person][1]),  # f ch_person_wear
                keys,  # s key1
                RT1 * 1000,  # f rt1
                # outcomes
                ProbsFruit[selected_person],  # f  exp_value_ch_fruit
                ResultFruit,  # f reward_fruit
                ProbsWear[selected_person],  # f exp_value_ch_wear
                ResultWear,  # f reward_ch_wear
                key2,  # s key2
                RT2 * 1000,  # f rt2
                key3,  # s key3
                RT3 * 1000,  # f rt3
                first_product,  # s first_product (fruit/wear)
                second_product,  # s second_product (fruit/wear)
                fruit_loc,  # s fruit_loc
                r1[t],  # f exp_value_fruit1
                r2[t],  # f exp_value_fruit2
                wear_loc,  # s wear_loc
                r3[t],  # f exp_value_wear1
                r4[t],  # f exp_value_wear2
                iti,  # f iti
            )
        )
    return


# the trials themselves.
# each 'mytrial' run = one trial of the task.
# Ntrls,iti,ch_deadline,iti: fdbck_ch1 ,fdbck_ch2,fdbck_ch3,outcome_ch2,outcome_ch3
num_instructions = 14
for instruction in range(1, num_instructions + 1):
    test_instructions = visual.ImageStim(
        win,
        image="instructions/instructions_test/Test" + str(instruction) + ".png",
        pos=[0, 0],
        interpolate=True,
    )
    test_instructions.draw()
    win.update()
    event.waitKeys(keyList=["space", "s", "k"])

start_quiz = visual.ImageStim(
    win,
    image="instructions/instructions_test/start_quiz" + ".png",
    pos=[0, 0],
    interpolate=True,
)
start_quiz.draw()
win.update()
event.waitKeys(keyList=["space"])
quiz1 = visual.ImageStim(
    win, image="instructions/quiz/quiz1" + ".png", pos=[0, 0], interpolate=True,
)
quiz1.draw()
win.update()
event.waitKeys(keyList=["s"])

quiz2 = visual.ImageStim(
    win, image="instructions/quiz/quiz2" + ".png", pos=[0, 0], interpolate=True,
)
quiz2.draw()
win.update()
event.waitKeys(keyList=["s"])
quiz3 = visual.ImageStim(
    win, image="instructions/quiz/quiz3" + ".png", pos=[0, 0], interpolate=True,
)
quiz3.draw()
win.update()
event.waitKeys(keyList=["k"])
quiz4 = visual.ImageStim(
    win, image="instructions/quiz/quiz4" + ".png", pos=[0, 0], interpolate=True,
)
quiz4.draw()
win.update()
event.waitKeys(keyList=["s"])

quiz5 = visual.ImageStim(
    win, image="instructions/quiz/quiz5" + ".png", pos=[0, 0], interpolate=True,
)
quiz5.draw()
win.update()
event.waitKeys(keyList=["k"])

start_training = visual.ImageStim(
    win,
    image="instructions/instructions_test/start_training.png",
    pos=[0, 0],
    interpolate=True,
)
start_training.draw()
win.update()
event.waitKeys(keyList=["space"])

mytrials(subject_num, "train", 2, 1, 6, 0.5, 0.5, 0.5, 1, 1)
start_test = visual.ImageStim(
    win,
    image="instructions/instructions_test/start_test.png",
    pos=[0, 0],
    interpolate=True,
)
start_test.draw()
win.update()
event.waitKeys(keyList=["space"])
mytrials(subject_num, "test", 25, 1, 6, 0.5, 0.5, 0.5, 1, 1)
finish_test = visual.ImageStim(
    win,
    image="instructions/instructions_test/finish_test.png",
    pos=[0, 0],
    interpolate=True,
)
finish_test.draw()
win.update()
event.waitKeys(keyList=["space"])
