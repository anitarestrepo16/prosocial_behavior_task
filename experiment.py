import numpy as np
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    decide_offer,
    present_offer,
    present_choice,
    translate_choice,
    work_rest_segment,
    present_feedback,
    get_MVC,
    fatigue_segment
)
from utils.write import (
    CSVWriter_trial,
	CSVWriter_block,
	CSVWriter_subj
) 
from utils.triggerer import Triggerer
from utils.gdx import gdx_vpython
from utils.gdx import gdx

#### initialize some things

# parport triggers
parport = Triggerer(0)
parport.set_trigger_labels(['MVC_start', 'MVC_end',
			     'baseline_start', 'baseline_end',
			     'fatigue_start', 'fatigue_end',
				   'show_offer', 'make_choice', 'work_rest', 'feedback'])

# hand dynamometer
grip = gdx.gdx()
grip.open(connection = 'usb', device_to_open = 'GDX-HD 15400221')
grip.select_sensors([1])

# data handling
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
trial_log = CSVWriter_trial(subj_num)
block_log = CSVWriter_block(subj_num)
subj_log = CSVWriter_subj(subj_num)
np.random.seed(subj_num)
points_self = 0
points_other = 0
trial_num = 1
block_num = 1

# practice trials
practice_trials = [
	'self_reward',
	'other_reward',
	'self_punishment',
	'other_punishment'
]

# make trials list
trials_per_type = 2
trials = [
	# self reward
    trials_per_type*['self_reward'] +
    # self punishment
	trials_per_type*['self_punishment'] +
	# other reward
	trials_per_type*['other_reward'] +
	# other punishment
	trials_per_type*['other_punishment']][0]
random.shuffle(trials)

# make blocks of trials
block1 = np.split(np.array(trials), 4)[0]
block2 = np.split(np.array(trials), 4)[1]
block3 = np.split(np.array(trials), 4)[2]
block4 = np.split(np.array(trials), 4)[3]

blocks = [block1, block2, block3, block4]

# psychopy viz
win = visual.Window(
	size = (1600, 1000),
	color = (0, 0, 0),
	colorSpace = 'rgb255',
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)
ANCHOR_Y = -0.5
MVC_TIME = 3
BASELINE_TIME = 3
OFFER_TIME = 1
FEEDBACK_TIME = 1
BREAK_TIME = 0.5

dynamo = visual.ImageStim(win, 'image_stim/Go_Direct_Dynomometer.jpg', pos = (0, -0.5))
grip_right = visual.ImageStim(win, 'image_stim/grip_right.jpg', pos = (0, -0.1))
choice_img = visual.ImageStim(win, 'image_stim/choice.png', pos = (0, -0.2))
rest_points = visual.ImageStim(win, 'image_stim/rest_points.PNG', pos = (-300, 0), size = (640, 360), units = "pix")
work_points = visual.ImageStim(win, 'image_stim/work_points.PNG', pos = (300, 0), size = (640, 360), units = "pix")

########################
# Maximum Voluntary Contraction (MVC)
########################

# Instructions 

dynamo.draw()
txt = '''
First we're going to measure your grip strength 3 times using
 the grip strength sensor (pictured below). \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

grip_right.draw()
txt = '''
\n
This is the way you should hold the grip strength sensor. 
Make sure your fingers are wrapped tightly around it like
in the picture. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n 
You will see a countdown on the screen from 3 to 1. Then the word SQUEEZE
will appear on the screen. As soon as you see this, squeeze the hand dynamometer 
as tightly as you can until the word STOP appears on the screen (~3 seconds). 
\n
Press the spacebar to see an example.
'''
wait_for_keypress(win, txt)

# Example MVC
present_text(win, '3')
present_text(win, '3, 2')
present_text(win, '3, 2, 1')
present_text(win, 'SQUEEZE', 'white', 3)
present_text(win, 'STOP', 'red', 0.5)

grip_right.draw()
txt = '''
\n
Position your dominant hand on the hand dynamometer now.\n
\n
\n
\n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Get MVC 1
parport.send_trigger('MVC_start')
max_grip = get_MVC(win, grip, MVC_TIME)
parport.send_trigger('MVC_end')
subj_log.write(subj_num, max_grip)

txt = '''
\n
Take a few seconds to rest.\n
Press the spacebar when you're ready to go again.
'''
wait_for_keypress(win, txt)

# Get MVC 2
parport.send_trigger('MVC_start')
max_grip = get_MVC(win, grip, MVC_TIME)
parport.send_trigger('MVC_end')
subj_log.write(subj_num, max_grip)

txt = '''
\n
Take a few seconds to rest.\n
Press the spacebar when you're ready to go again.
'''
wait_for_keypress(win, txt)

# Get MVC 3
parport.send_trigger('MVC_start')
max_grip = get_MVC(win, grip, MVC_TIME)
parport.send_trigger('MVC_end')
subj_log.write(subj_num, max_grip)

########################
# Baseline Physio
########################

# Instructions
txt = '''
\n
Now you will sit quietly for 5 minutes. 
The word RELAX will appear on the screen. Just sit comfortably,
 relax and breathe normally. The screen will let you know when it is time
 for the next task. \n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Get Baseline Physio
parport.send_trigger('baseline_start')
present_text(win, 'Relax', BASELINE_TIME)
parport.send_trigger('baseline_end')

########################
# Prosocial Behavior Task
########################

t1 = time()

# Instructions
txt = '''
\n
Now we will play a game. For some rounds you'll be playing
for yourself and for other rounds you'll be playing for the next
participant.
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
in the game you will win or lose points by squeezing the 
grip strength sensor. The number of points you win will determine
how much extra cash you get to take home.
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
For half the rounds, the points will go to YOU while for the other
half of the rounds the points go to the NEXT PARTICIPANT. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
The points that the previous participant won for you will 
be added to the points you win during the game for an extra cash prize. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
At the start of each round you will see an "Offer" on the screen
that tells you who the points earned during that round will go to. 
You will see either YOU or NEXT PARTICIPANT. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
The "Offer" at the start of each round will also 
tell you whether you are playing to EARN or AVOID LOSING points
during that round. 
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)


# Sample Offer
str1 = visual.TextStim(win, "Here is an example \"Offer\":\n")
str2 = visual.TextStim(win, "Offer: Work to", color = 'white', pos = (0, 0.6))
type_txt = visual.TextStim(win, 'AVOID LOSING', color = 'forestgreen',pos = (0, 0.4))
str3 = visual.TextStim(win, "10 points for", color = 'white', pos = (0, 0.2))
target_txt = visual.TextStim(win, 'THE NEXT PARTICIPANT', color = 'purple', pos = (0, 0))
str4 = visual.TextStim(win, 'Press the spacebar to continue.', color = 'white', pos = (0, -0.4))
str1.draw()
str2.draw()
type_txt.draw()
str3.draw()
target_txt.draw()
str4.draw()
win.flip()
event.waitKeys(keyList = ["space"]) # wait until subject responds

choice_img.draw()
txt = '''
\n
Once you see the "Offer", you have the option to either WORK to obtain
the "Offer" or REST. This is what the choice screen looks like: \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

choice_img.draw()
txt = '''
\n
To choose WORK, you press the left arrow key. To choose REST, you 
press the right arrow key. \n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need target image
txt = '''
\n
If you choose to WORK, you succeed by squeezing the grip sensor
to a predetermined TARGET level for 1 second. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

####### need target image
txt = '''
\n
If you don't squeeze at or above the TARGET level for 1 second 
you will fail the round. If you don't squeeze 
at or above the TARGET you will fail the trial. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
If you choose to REST, you will
just sit quietly for 3 seconds. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
After each round, you will receive feedback on the points
won or lost for that round. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
If you choose to WORK and succeed, you will win 10 points
for an EARN round or lose 0 points for an AVOID LOSING round. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
If you choose to WORK and fail, you will win 0 points
for an EARN round or lose 10 points for an AVOID LOSING round. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need work EARN success pic
txt = '''
\n
For example, if you choose to WORK to EARN 10 points
and succeed, you will successfully earn the 10 points. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need work EARN fail pic
txt = '''
\n
But if you choose to WORK to EARN 10 points
and fail, you will not earn the 10 points. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need work AVOID LOSING success pic
txt = '''
\n
If you choose to WORK to AVOID LOSING 10 points
and succeed, you will successfully avoid losing the 10 points. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need work AVOID LOSING fail pic
txt = '''
\n
But if you choose to WORK to AVOID LOSING 10 points
and fail, you will lose the 10 points. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
If you choose to REST, you earn fewer points than if you chose to
WORK and succeeded. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need rest EARN pic
txt = '''
\n
For example, if the offer is to EARN points and you choose to REST,
you will earn 1 point. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

###### need rest AVOID LOSING pic
txt = '''
\n
If the offer is to AVOID LOSING points and you choose to REST,
you will lose 1 point. \n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

rest_points.draw()
work_points.draw()
txt = '''
\n
For any type of round, choosing to REST results in better outcomes 
than choosing to WORK and failing but worse outcomes than 
choosing to WORK and succeeding. \n
 \n
 \n
 \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

#### Need pic
txt = '''
\n
So for an EARN round, choosing to WORK and succeeding gives you the 
most points. Choosing to WORK and failing gives you the least points. \n
 \n
 \n
 \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

#### Need pic
txt = '''
\n
For an AVOID LOSING round, choosing to WORK and succeeding results 
in the least points lost. Choosing to WORK and failing results 
in the most points lost. \n
 \n
 \n
 \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
\n
Let's do a practice run. Hold the grip strength sensor in your dominant 
hand. \n
Press the spacebar when you're ready for the practice round.
'''
wait_for_keypress(win, txt)

# Practice
for trial in practice_trials:
	# offer
	type, target = decide_offer(trial)
	present_offer(win, type, target, OFFER_TIME)
	# fixation
	fixation_cross(win)
	# choice
	choice = present_choice(win)
	# fixation
	fixation_cross(win)
	# work/rest
	avg_grip, success = work_rest_segment(win, choice, grip, max_grip, ANCHOR_Y)
	# fixation
	fixation_cross(win)
	# feeback
	points = present_feedback(win, trial, choice, success, FEEDBACK_TIME)
	# fixation (ITI)
	fixation_cross(win)

txt = '''
Now you're ready for the real game. Every couple rounds you'll be asked 
to rate how fatigued your hand is and will 
be able to take a short break. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
Make sure to hold the grip strenmgth sensor only in your dominant 
hand throughout the task. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
We'll start with a measure of hand fatigue. 
Use the mouse to rate your fatigue on the scale from 0 to 100. \n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Run Prosocial Behavior Task

# baseline fatigue rating
parport.send_trigger('fatigue_start')
fatigue_rating = fatigue_segment(win)
parport.send_trigger('fatigue_start')
block_log.write(0, fatigue_rating)
wait_for_keypress(win, 'Press the spacebar to start the task.')

# cycle through blocks
for block in blocks:

	for trial in block:

		# decide what to offer this trial
		type, target = decide_offer(trial)
		# show offer
		parport.send_trigger('show_offer')
		present_offer(win, type, target, OFFER_TIME)
		# fixation
		fixation_cross(win)
		# choice
		choice = present_choice(win)
		parport.send_trigger('make_choice')
		# fixation
		fixation_cross(win)
		# work/rest
		parport.send_trigger('work_rest')
		avg_grip, success = work_rest_segment(win, choice, grip, max_grip, ANCHOR_Y)
		print(success)
		# fixation
		fixation_cross(win)
		# feeback
		parport.send_trigger('feedback')
		points = present_feedback(win, trial, choice, success, FEEDBACK_TIME)
		# keep track of point changes
		points_self += points[0]
		points_other += points[1]
		# fixation (ITI)
		fixation_cross(win)

		# save data
		choice = translate_choice(choice)
		trial_log.write(
			block_num,
			trial_num,
			trial,
			choice,
			avg_grip, 
			success,
			points[0],
			points[1]
		)
		trial_num += 1
		# trial end

	# fatigue rating
	parport.send_trigger('fatigue_start')
	fatigue_rating = fatigue_segment(win)
	parport.send_trigger('fatigue_start')
	block_log.write(block_num, fatigue_rating)

	# short break
	present_text(win, 'You can take a short break now.', 'white', BREAK_TIME)
	wait_for_keypress(win, 'Press the spacebar to continue the task.')
	block_num += 1
	# block end

grip.close()
t2 = time()
print('Task Complete.')
print('The task took %d minutes.'%((t2 - t1)/60))
print('Participant earned %d points for themselves.'%(points_self))
print('Participant earned %d points for the next participant.'%(points_other))

##########################
# and we're done!
##########################
txt = '''
That's all! You can press the spacebar to end the experiment.
If the experimenter doesn't come get you immediately, let them
know you're done using the button on your desk.
'''
wait_for_keypress(win, txt)
