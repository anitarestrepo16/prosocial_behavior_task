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
    present_feedback
)
from utils.write import CSVWriter
from utils.triggerer import Triggerer
from gdx import gdx

# initialize some things
parport = Triggerer(0)
grip = gdx.gdx()
grip.open(connection = 'usb', device_to_open = 'GDX-HD 15400221')
grip.select_sensors([1])
parport.set_trigger_labels(['show_offer', 'make_choice', 'work_rest', 'feedback'])
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
log = CSVWriter(subj_num)
np.random.seed(subj_num)
max_grip = input("Enter max voluntary contraction: ")
max_grip = float(max_grip)


# make trials list
trials_per_block = 1
trials = [
	# self reward
    trials_per_block*['self_reward'] +
    # self punishment
	trials_per_block*['self_punishment'] +
	# other reward
	trials_per_block*['other_reward'] +
	# other punishment
	trials_per_block*['other_punishment']][0]
random.shuffle(trials)

points_self = 0
points_other = 0
trial_num = 1


win = visual.Window(
	size = (800, 600),
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)

t1 = time()

########################
# instructions
########################
txt = '''
Instructions go here.
(press spacebar to continue through instructions)
'''
wait_for_keypress(win, txt)



########################
# experiment
########################
for trial in trials:

	## decide what to offer this trial
	offer = decide_offer(trial)

	## now actually run the trial
	# offer
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
	avg_grip, success = work_rest_segment(win, choice, grip, max_grip)
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
	choice = translate_choice(choice)
	log.write(
		trial_num,
		trial,
		offer,
		choice,
		success,
		points[0],
		points[1]
	)
	trial_num += 1

grip.close()
t2 = time()
print('Experiment Complete.')
print('The experiment took %d minutes.'%((t2 - t1)/60))
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
