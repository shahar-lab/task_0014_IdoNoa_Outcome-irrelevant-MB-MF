from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
import random, serial, time
from random import sample
import numpy as np


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
    "subject,trial, step, Presented Person, Smpled-Stim, SmpledStim-Location, FalseStim, FalseStim-Location, Pressed Key, Reaction Time\n"
)
win = visual.Window(
    monitor="testMonitor", units="deg", screen=0, color=(255, 255, 255), fullscr=True
)
win.mouseVisible = False

humanLst = [
    "m1.png",
    "m2.png",
    "w1.png",
    "w2.png",
    "m1.png",
    "m2.png",
    "w1.png",
    "w2.png",
]
fruitwear = [
    "f1.png",
    "f2.png",
    "f2.png",
    "f1.png",
    "c1.png",
    "c2.png",
    "c1.png",
    "c2.png",
]
fixation = visual.TextStim(win, text="+", pos=[0, 0], color=(0, 0, 0))
memory_refresh = visual.ImageStim(
    win,
    image="instructions/instructions_training/refresh_memory.png",
    pos=[0, 0],
    interpolate=True,
)
P1 = ["m1.png", "f1.png", "c1.png"]
P2 = ["w2.png", "f1.png", "c2.png"]
P3 = ["w1.png", "f2.png", "c1.png"]
P4 = ["m2.png", "f2.png", "c2.png"]
AllP = [P1, P2, P3, P4]
SampleStims = ["f1.png", "f2.png", "c1.png", "c2.png"]

# הוראות
kb = keyboard.Keyboard()
kb.start()
num_instructions = 4
for instruction in range(1, num_instructions + 1):
    prac_instructions = visual.ImageStim(
        win,
        image="instructions/instructions_training/Training" + str(instruction) + ".png",
        pos=[0, 0],
        interpolate=True,
    )
    prac_instructions.draw()
    win.update()
    event.waitKeys(keyList=["space", "s", "k"])

trial = 0
count_false = 0
restart = True

while restart == True:
    trial = trial + 1
    if trial % 4 == 0:
        memory_refresh.draw()
        win.update()
        event.waitKeys(keyList=["space"])
    count_true = 0
    indices = [0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 4, 5, 6, 7]
    indices = np.array(indices)
    np.random.shuffle(indices)

    for i in indices:
        keys = kb.getKeys(["escape"])
        if "escape" in keys:
            win.close()
            core.quit()
        WrongStims = ["f1.png", "f2.png", "c1.png", "c2.png"]
        for j in AllP:
            if j[0] == humanLst[i]:
                print(WrongStims)
                WrongStims.remove(j[1])
                WrongStims.remove(j[2])
                print(WrongStims)
                break
        rndsmple = [4, -4]
        rndlocation = np.random.choice(rndsmple, 2, replace=False)
        HumansSmpledStim = visual.ImageStim(win, image=humanLst[i], pos=[0, 5])
        SmpledStim = visual.ImageStim(win, image=fruitwear[i], pos=[rndlocation[0], 0])
        WrongStim = visual.ImageStim(
            win, image=random.choice(WrongStims), pos=[rndlocation[1], 0]
        )
        Tooslow = visual.TextStim(
            win,
            text="Too slow, the task is started from the beginning.",
            pos=[0, 0],
            color=(0, 0, 0),
        )
        Wrongchoice = visual.TextStim(
            win,
            text=("Wrong choice, the task is started from the beginning"),
            pos=[0, 0],
            color=(0, 0, 0),
        )
        Goodchoice = visual.TextStim(
            win, text=("Good job!"), pos=[0, 0], color=(0, 0, 0)
        )
        count_true += 1
        countxt = count_true
        counter = visual.TextStim(
            win,
            text=(str(count_true) + "/16"),
            pos=[0, -5],
            height=0.5,
            color=(0, 0, 0),
        )
        print(rndlocation)
        if rndlocation[0] == (-4):
            TrueLoc = ["s"]
        else:
            TrueLoc = ["k"]

        fixation.draw()
        win.update()
        core.wait(0.5)
        counter.autoDraw = True
        HumansSmpledStim.draw()
        SmpledStim.draw()
        WrongStim.draw()
        win.update()
        myclock = core.Clock()
        choice = event.waitKeys(maxWait=8)
        RT = myclock.getTime()
        print(RT)
        counter.autoDraw = False
        humanData = humanLst[i]
        humanData = humanData.replace(".png", "")
        fruitwearData = fruitwear[i]
        fruitwearData = fruitwearData.replace(".png", "")
        wrongStimData = WrongStim.image
        wrongStimData = wrongStimData.replace(".png", "")
        dataFile.write(
            "%i,%i,%i,%s,%s,%i,%s,%i,%s,%i\n"
            % (
                subject_num,
                trial,
                count_true,
                humanData,
                fruitwearData,
                rndlocation[0],
                wrongStimData,
                rndlocation[1],
                choice,
                RT * 1000,
            )
        )
        # check if correct and fast enough
        if choice == TrueLoc and RT <= 2.5:
            HumansSmpledStim.draw()
            SmpledStim.draw()
            win.update()
            core.wait(1)
            Goodchoice.draw()
            win.update()
            core.wait(1.0)
            if count_true == 16:
                restart = False
        elif RT >= 2.5:  # too slow
            count_false += 1
            Tooslow.draw()
            win.update()
            core.wait(1)
            break
        else:  # wrong choice
            count_false += 1
            Wrongchoice.draw()
            win.update()
            core.wait(1)
            break
finish_training = visual.ImageStim(
    win,
    image="instructions/instructions_training/Training5.png",
    pos=[0, 0],
    interpolate=True,
)
finish_training.draw()
win.update()
event.waitKeys(keyList=["space"])

