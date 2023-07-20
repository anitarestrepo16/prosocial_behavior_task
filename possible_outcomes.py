import numpy as np
from psychopy import visual, event, core
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



# practice trials
practice_trials = [
	'self_reward',
	'other_reward',
	'self_punishment',
	'other_punishment'
]

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
BREAK_TIME = 0.5

dynamo = visual.ImageStim(win, 'Go_Direct_Dynomometer.jpg', pos = (0, -0.5))
grip_right = visual.ImageStim(win, 'grip_right.jpg', pos = (0, -0.5))


def present_feedback(win, trial, choice, success):
	'''
	Present text with points lost or gained and return
		number of points.
	'''
	# default
	outcome = 'nothing'
	target =  'no one'
	# if chose rest
	if ('right' in choice):
		# if self reward trial
		if (trial == 'self_reward'):
			outcome = "+1 point for"
			target = 'YOU'
			points_self = 1
			points_other = 0
		# if other reward trial
		elif (trial == 'other_reward'):
			outcome = "+1 point for"
			target = 'THE NEXT PARTICIPANT'
			points_self = 0
			points_other = 1
		# if self punishment trial
		elif (trial == 'self_punishment'):
			outcome = "-1 point for"
			target = 'YOU'
			points_self = -1
			points_other = 0
		# if other punishment trial
		elif (trial == 'other_punishment'):
			outcome = "-1 point for"
			target = 'THE NEXT PARTICIPANT'
			points_self = 0
			points_other = -1
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0
	
	# if worked and succeeded
	elif ('left' in choice) & (success):
		if trial == 'self_reward':
			outcome = "Success! \n +10 points for"
			target = 'YOU'
			points_self = 10
			points_other = 0
		elif trial == 'self_punishment':
			outcome = "Success! \n -0 points for"
			target = 'YOU'
			points_self = 0
			points_other = 0
		elif trial == 'other_reward':
			outcome = 'Success! \n +10 points for'
			target = 'THE NEXT PARTICIPANT'
			points_self = 0
			points_other = 10
		elif trial == 'other_punishment':
			outcome = 'Success! \n -0 points for'
			target = 'THE NEXT PARTICIPANT'
			points_self = 0
			points_other = 0
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0

	# if worked and failed
	elif ('left' in choice) & (not success):
		if trial == 'self_reward':
			outcome = "Failed. \n +0 points for"
			target = 'YOU'
			points_self = 0
			points_other = 0
		elif trial == 'self_punishment':
			outcome = "Failed. \n -10 points for"
			target = 'YOU'
			points_self = -10
			points_other = 0
		elif trial == 'other_reward':
			outcome = 'Failed. \n +0 points for'
			target = 'THE NEXT PARTICIPANT'
			points_self = 0
			points_other = 0
		elif trial == 'other_punishment':
			outcome = 'Failed. \n -10 points for'
			target = 'THE NEXT PARTICIPANT'
			points_self = 0
			points_other = -10
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0
	
	if target == 'YOU':
		target_col = 'gold'
	elif target == 'THE NEXT PARTICIPANT':
		target_col = 'mediumslateblue'

	# sanity check
	if points_self != 0:
		assert points_other == 0
	if points_other != 0:
		assert points_self == 0
	
	outcome_txt = visual.TextStim(win, outcome, color = 'white',
					pos = (0, 0.4))
	target_txt = visual.TextStim(win, target, color = target_col,
					pos = (0, 0))
	outcome_txt.draw()
	target_txt.draw()
	win.flip()
	event.waitKeys(keyList = ["space"])
	return (points_self, points_other)

# Practice
for trial in practice_trials:
	# offer
	offer = decide_offer(trial)
	wait_for_keypress(win, offer)
	# choice
	choice = present_choice(win)
	# feeback
	present_feedback(win, trial, choice, 1)


