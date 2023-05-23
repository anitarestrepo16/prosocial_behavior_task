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
Instructions for getting MVC.
(press spacebar to continue through instructions)
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
Instructions for Baseline Physio.
(press spacebar to continue through instructions)
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
Instructions for task.
(press spacebar to continue through instructions)
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
	present_text(win, 'You can take a short break now.', BREAK_TIME)
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
