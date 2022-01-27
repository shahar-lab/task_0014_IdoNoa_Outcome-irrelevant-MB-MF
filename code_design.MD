This task was built using <a href="https://www.psychopy.org/">psychopy</a>.

The experiment starts when participants are told that they own a business and that the persons in the image below are their salespersons. 

![image](https://user-images.githubusercontent.com/51457131/151413177-18bb9da4-a6cb-44c3-b244-d9eff4a72475.png)

As can be seen in the image, each salesperson is able to sell the objects appearing below him. 

The code starts with a training part (training_for_rani_task.py), in which the participants learn the model of the task. 

Specifically, they are shown each training trial a salesperson with two objects, that only one of which is being sold by this person.
Subjects need to make 16 consecutive correct answers regarding which object is being sold by the shown sales person, in less than 2.5 seconds.
Only after completing the training, they will continue to the test part.

In the test part (ranitask.py) participants have to choose on each trial between two offered salesperson. 
![image](https://user-images.githubusercontent.com/51457131/151417832-bc69efa9-89b9-4632-a498-d1de0851ba91.png)
After selecting a salesperson, the objects of the chosen person will appear one after the other in a random order, marked by a red rectangle.
When the rectangle appears around an object, the participant should press the 's' or 'k' key (according to the object's location) to discover whether it was sold. 
Subjects can get a monetary bonus for successful sales.
![image](https://user-images.githubusercontent.com/51457131/151418001-b1a4232c-344d-43dd-9240-da6f7ab6c482.png)


The script includes a main function called mytrials() which runs a loop of 40 trials over 5 blocks. 

There is a small break in between blocks, but the random walk continues from the same point.

In each trial, two persons are randomly sampled by the computer. 

In addition, we also randomly sample the locations of the shops in this stage, as they are not affected by participants' behavior.

Only after getting ch_key1 we are ready to insert the matching as the fruit and wear images.
Additionally, the reward probability is decided by the chosen objects.

In every step, pressing a wrong button (such as one not reflecting the location of the shop) will abort the trial and write the current data to the csv file.
Participants can take a break in the person choice stage by pressing 'space' - which will also abort the trial and write the current data to the csv.

Other than the main function, the script includes an instructions part which is simply showing pictures. 

The quiz part is simply showing pictures and only letting them move forward by picking the right option.

