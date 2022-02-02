This repository includes two tasks: training.py and main.py

training.py is self-contained and runs the model-training part.

main.py builds upon the function trial.py and the utils.py functions and runs the RL task.

The main task runs a trials loop in trial.py. 

Training part of main task is 10 trials in one block. 

Test part of main task is 50 trials in each of 4 blocks so 200 trials in total.

At the end of each block participants have a break which they can terminate at their own time (game_pause_func in utils.py)

The instructions and quiz functions are called in main.py.

In each trial of the trial.py loop, two persons are randomly sampled by the computer (stimuli function from utils.py). 

In addition, we also randomly sample the locations of the shops in this stage, as they are not affected by participants' behavior.

Only after getting the response from the participants (choice in utils.py) we get the stimuli of the objects (stimuli_by_choice in utils.py).

Furthermore, the reward probability is decided by the chosen objects (draw_reward function in utils.py).

In every step, pressing a wrong button (wrong_key_func in utils.py) or too slow of a reaction (too_slow in utils.py) will abort the trial and write the current data to the csv file (update_data functions in utils.py). Additionally, participants can have a break by pressing "space" in the choice part which will also abort the trial(call_supervisor in utils.py).

data is saved using the save_data function from utils.py.

A csv file is saved locally with the headers created in main.py.
