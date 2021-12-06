from psychopy import core, visual, gui, data, event, clock, monitors
from psychopy.hardware import keyboard
import numpy as np

# create a text file to save data
expInfo = {"subject": "999"}
dlg = gui.DlgFromDict(expInfo, title="Two-armed bandit task")
fileName = "ranitask" + expInfo["subject"] + "_" + data.getDateStr()
monitor_size = monitors.Monitor("testMonitor").getSizePix()
dataFile = open(
    fileName + ".csv", "w"
)  # a simple text file with 'comma-separated-values'
dataFile.write(
    "phase,trial, Lperson, Rperson, Key1, RT1, ChosenP,Items for sale in trial, Probs-Veg, Fdbck-Veg, Ch2-Key, Ch2-RT, Probs-Wear, Fdbck-Wear, Ch3-Key, Ch3-RT, Veg/Wear 1st,iti\n"
)
win = visual.Window(
    monitor="testMonitor", screen=0, units="deg", color=(255, 255, 255), fullscr=True
)
win.mouseVisible = False
# ser = serial.Serial("COM3", 9600)


humansLst = ["m1.png", "m2.png", "w1.png", "w2.png"]
vegetable = ["v1.png", "v2.png", "v2.png", "v1.png"]
wear = ["c1.png", "c2.png", "c1.png", "c2.png"]
cond = [3, 6]
rndsmple = [3, -3]
SelectedPerson = None
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
rwalk = np.genfromtxt("rndwalk/rndwalk.csv", delimiter=",")
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
    phase,
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
    for t in range(1, Ntrls + 1):
        if t % 50 == 0:
            game_pause.draw()
            win.update()
            event.waitKeys(keyList=["space"])
        keys = kb.getKeys(["escape"])
        if "escape" in keys:
            win.close()
            core.quit()
        SampledStim = np.random.choice(4, 2, replace=False)
        rndlocation = np.random.choice(rndsmple, 2)

        # define the stimuli
        LStim = visual.ImageStim(
            win, image=humansLst[SampledStim[0]], pos=[-6, 5], interpolate=True
        )
        RStim = visual.ImageStim(
            win, image=humansLst[SampledStim[1]], pos=[6, 5], interpolate=True
        )
        VegStim = visual.ImageStim(
            win, image=vegetable[0], pos=[rndlocation[0], 0], size=2
        )
        WearStim = visual.ImageStim(
            win, image=wear[0], pos=[rndlocation[1], -5], size=2
        )
        VegCvr = visual.ImageStim(win, image="veg.png", pos=[rndlocation[0], 0])
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
        VegCvr.draw()
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
                "%s,%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                )
            )
            continue
        keys, RT1 = keysEvent[0]

        # set the variables by the selected choice (left or right)
        if keys == "s":
            SelectedPerson = SampledStim[0]
            VegStim.image = vegetable[SelectedPerson]
            WearStim.image = wear[SelectedPerson]
            PresentedStim = LStim
        elif keys == "k":
            SelectedPerson = SampledStim[1]
            VegStim.image = vegetable[SelectedPerson]
            WearStim.image = wear[SelectedPerson]
            PresentedStim = RStim
        elif keys == "space":
            dataFile.write(
                "%s,%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
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
                "%s,%i,%i,%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                )
            )
            continue
        trialStims = (VegStim.image + WearStim.image).replace(".png", "")
        ProbsVeg = [r1[t], r2[t], r2[t], r1[t]]
        ProbsWear = [r3[t], r4[t], r3[t], r4[t]]
        print(ProbsVeg[SelectedPerson])
        print(ProbsWear[SelectedPerson])
        # check if won/lost by predetermined probablity of SelectedPerson
        if np.random.random() < ProbsVeg[SelectedPerson]:
            RewardVeg = won
            ResultVeg = 1
        else:
            RewardVeg = lost
            ResultVeg = 0
        if np.random.random() < ProbsWear[SelectedPerson]:
            RewardWear = won
            ResultWear = 1
        else:
            RewardWear = lost
            ResultWear = 0

        # Counterbalance of stim presentation - Vegtables first or Clothing first.
        topFirst = np.random.choice(("VegFirst", "WearFirst"), 1)
        if topFirst == "VegFirst":
            FirstRecDraw = (-0.7, 0.7, -0.24, 0.26)
            SecRecDraw = (-0.7, 0.7, -0.78, -0.24)
            Draw12 = (VegStim, WearCvr)
            Draw3 = (VegCvr, WearCvr)
            Draw456 = (VegCvr, WearStim)
            Reward1 = RewardVeg
            Reward2 = RewardWear
            Rpos1 = 0
            Rpos2 = -5
            FrstLocation = VegStim.pos[0]
            ScndLocation = WearStim.pos[0]

        else:
            FirstRecDraw = (-0.7, 0.7, -0.78, -0.24)
            SecRecDraw = (-0.7, 0.7, -0.24, 0.26)
            Draw12 = (VegCvr, WearStim)
            Draw3 = (VegCvr, WearCvr)
            Draw456 = (VegStim, WearCvr)
            Reward1 = RewardWear
            Reward2 = RewardVeg
            Rpos1 = -5
            Rpos2 = 0
            FrstLocation = WearStim.pos[0]
            ScndLocation = VegStim.pos[0]

        # the task itself, drawing the stimuli and the feedbacks
        PresentedStim.autoDraw = True
        VegCvr.draw()
        WearCvr.draw()
        rect(-0.7, 0.7, 0.3, 0.7)
        win.flip()
        core.wait(fdbck_ch1)
        VegCvr.draw()
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
                "%s,%i,%i,%i,%s,%i,%i,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    keys,
                    RT1 * 1000,
                    SelectedPerson + 1,
                    trialStims,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
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
            dataFile.write(  # write trial data and continue
                "%s,%i,%i,%i,%s,%i,%i,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    keys,
                    RT1 * 1000,
                    SelectedPerson + 1,
                    trialStims,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
                    np.nan,
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
            if topFirst == ["VegFirst"]:
                ProbsWear = [np.nan, np.nan, np.nan, np.nan]
                ResultWear = np.nan
            else:
                ProbsVeg = [np.nan, np.nan, np.nan, np.nan]
                ResultVeg = np.nan
            PresentedStim.autoDraw = False
            Tooslow.draw()
            win.update()
            core.wait(1)
            dataFile.write(
                "%s,%i,%i,%i,%s,%i,%i,%s,%f,%f,%s,%i,%f,%f,%f,%f,%s,%i\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    keys,
                    RT1 * 1000,
                    SelectedPerson + 1,
                    trialStims,
                    ProbsVeg[SelectedPerson] * 100,
                    ResultVeg,
                    key2,
                    RT2 * 1000,
                    ProbsWear[SelectedPerson] * 100,
                    ResultWear,
                    np.nan,
                    np.nan,
                    topFirst,
                    iti,
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
            if topFirst == ["VegFirst"]:
                ProbsWear = [np.nan, np.nan, np.nan, np.nan]
                ResultWear = np.nan
            else:
                ProbsVeg = [np.nan, np.nan, np.nan, np.nan]
                ResultVeg = np.nan
            dataFile.write(
                "%s,%i,%i,%i,%s,%i,%i,%s,%f,%f,%s,%i,%f,%f,%f,%f,%s,%i\n"
                % (
                    phase,
                    t,
                    SampledStim[0] + 1,
                    SampledStim[1] + 1,
                    keys,
                    RT1 * 1000,
                    SelectedPerson + 1,
                    trialStims,
                    ProbsVeg[SelectedPerson] * 100,
                    ResultVeg,
                    key2,
                    RT2 * 1000,
                    ProbsWear[SelectedPerson] * 100,
                    ResultWear,
                    np.nan,
                    np.nan,
                    topFirst,
                    iti,
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
            "%s,%i,%i,%i,%s,%i,%i,%s,%i,%i,%s,%i,%i,%i,%s,%i,%s,%i\n"
            % (
                phase,
                t,
                SampledStim[0] + 1,
                SampledStim[1] + 1,
                keys,
                RT1 * 1000,
                SelectedPerson + 1,
                trialStims,
                ProbsVeg[SelectedPerson] * 100,
                ResultVeg,
                key2,
                RT2 * 1000,
                ProbsWear[SelectedPerson] * 100,
                ResultWear,
                key3,
                RT3 * 1000,
                topFirst,
                iti,
            )
        )
    return


# the trials themselves.
# each 'mytrial' run = one trial of the task.
# Ntrls,iti,ch_deadline,fdbck_ch1,fdbck_ch2,fdbck_ch3,outcome_ch2,outcome_ch3
num_instructions = 15
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
mytrials("train", 10, 1, 6, 0.5, 0.5, 0.5, 1, 1)
start = visual.ImageStim(
    win,
    image="instructions/instructions_test/start_test.png",
    pos=[0, 0],
    interpolate=True,
)
start.draw()
win.update()
event.waitKeys(keyList=["space"])
mytrials("test", 150, 1, 6, 0.5, 0.5, 0.5, 1, 1)

