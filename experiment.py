import numpy as np
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    decide_offer,
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
	size = (800, 600),
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
BREAK_TIME = 0.5

########################
# Maximum Voluntary Contraction (MVC)
########################

# Instructions  
txt = '''
First we're going to measure your maximum grip strength. 
Grab the hand dynamometer with your dominant hand so that the 
blue pieces are at the top and the cable is coming out the bottom
of the device. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
Wrap your hand around the dynamometer so
that the heel of your palm is against the bottom long blue piece
and your fingers wrap around the top blue piece.\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
After a short countdown, please squeeze the hand dynamometer 
as tightly as you can until the screen switches to the next task. 
Position your dominant hand on the hand dynamometer now.\n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Get MVC
parport.send_trigger('MVC_start')
max_grip = get_MVC(win, grip, MVC_TIME)
parport.send_trigger('MVC_end')
subj_log.write(subj_num, max_grip)

########################
# Baseline Physio
########################

# Instructions
txt = '''
Now we are going to collect a 5-minute baseline measurement for the ECG. 
Sit comfortably, relax and breathe normally. \n
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
We are now going to begin the main part of the experiment. 
For each trial in this task you will be given an offer to work to 
either earn points or avoid losing points. You will then be given 
the choice to either "work" or "rest". \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
If you choose to work, you'll be asked to squeeze the hand dynamometer
to a target level for 3 seconds. If you succeed, you will successfully
obtain the offer. For some offers, the points earned or lost will be applied 
to you while for other offers the points will go to the next participant. You'll
be told who the target of the offer is at the beginning of each trial. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
After each trial, you will receive feedback as to whether you succeeded
or failed (if you decided to work) and the number of points earned or lost
for the trial's target. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

txt = '''
Let's do a practice run. Grip the hand dynamometer in your dominant 
hand. \n
Press the spacebar when you're ready for the practice round.
'''
wait_for_keypress(win, txt)

# Practice
for trial in practice_trials:
	# offer
	offer = decide_offer(trial)
	present_text(win, offer)
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
	points = present_feedback(win, trial, choice, success)
	# fixation (ITI)
	fixation_cross(win)

txt = '''
Now you're ready for the real task. You will complete a total of 100 trials. 
After every 25 trials you'll be asked to rate your fatigue levels and will 
be able to take a short break. Make sure to hold the hand dynamometer
exclusively in your dominant hand throughout the task. We'll start
with a fatigue rating. \n
Press the spacebar when you're ready to begin.
'''
wait_for_keypress(win, txt)

# Run Prosocial Behavior Task

# baseline fatigue rating
parport.send_trigger('fatigue_start')
fatigue_rating = fatigue_segment(win)
parport.send_trigger('fatigue_start')
block_log.write(0, fatigue_rating)

# cycle through blocks
for block in blocks:

	for trial in block:

		# decide what to offer this trial
		offer = decide_offer(trial)
		# show offer
		parport.send_trigger('show_offer')
		present_text(win, offer)
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
		points = present_feedback(win, trial, choice, success)
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
			offer,
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
