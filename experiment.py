import numpy as np
from collections import OrderedDict
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    present_choice,
    work_rest_segment,
    present_feedback
)



# initialize some things
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
#log = TSVWriter(subj_num)
np.random.seed(subj_num)
# targets
target_self = "you"
target_other = "the next participant"
targets = [target_self, target_other]
# trial types
offer_reward = "Exert Effort to Win 10 Points for "
offer_punishment = "Exert Effort to Avoid Losing 10 Points for "
offers = [offer_reward, offer_punishment]

# outcomes
win_reward = "+10 Points for "
win_punishment = "-0 Points for "
lose_reward = "-0 Points for "
lose_punishment = "-10 Points for "
outcomes = [win_reward, win_punishment, lose_reward, lose_punishment]

# make trials list

self_reward = ('self', 'reward') 
self_punishment = ('self', 'punishment') 
other_reward = ('other', 'reward')
other_punishment = ('other', 'punishment')

trials_per_block = 25
trials = [
	# self reward
    trials_per_block*(["self_reward"]) +
    # self punishment
	trials_per_block*['self_punishment'] +
	# other reward
	trials_per_block*['other_reward'] +
	# other punishment
	trials_per_block*['other_punishment']][0]
random.shuffle(trials)

points_self = 0
points_other = 0


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

	# decide what to offer this trial
	if trial == 'self_reward':
		offer = offer_reward + target_self
	elif trial == 'self_punishment':
		offer = offer_punishment + target_self
	elif trial == 'other_reward':
		offer = offer_reward + target_other
	elif trial == 'other_punishment':
		offer = offer_punishment + target_other
	else:
		offer = "Warning, wrong input"

	## now actually run the trial
	# offer
	present_text(win, offer)
	# fixation
	fixation_cross(win)
	# choice
	choice = present_choice(win)
	# fixation
	fixation_cross(win)
	# work/rest
	work_rest_segment(win, choice)
	#### need to figure out how will determine whether work trial succeeded
	success = True
	# fixation
	fixation_cross(win)
	# feeback
	points = present_feedback(win, trial, choice, success)
	# keep track of point changes
	points_self += points[0]
	points_other += points[1]
	# fixation (ITI)
	fixation_cross(win)


t2 = time()
print('Experiment Complete.')
print('The experiment took %d minutes.'%((t2 - t1)/60))

##########################
# and we're done!
##########################
txt = '''
That's all! You can press the spacebar to end the experiment.
If the experimenter doesn't come get you immediately, let them
know you're done using the button on your desk.
'''
wait_for_keypress(win, txt)
