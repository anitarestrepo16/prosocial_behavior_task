from psychopy import visual, core, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
from time import time

def fixation_cross(win):
	'''
	Displays a fixation cross for a random amount of time between
	200 and 400 milliseconds.
	'''
	fixation = visual.TextStim(win, text = '+', color = "white", pos = (0,0))
	fixation.draw()
	win.flip()
	core.wait(np.random.uniform(.2, .4))

def present_text(win, text_block, display_time = 1):
	'''
	Displays a block of text on the screen.
	'''
	msg = visual.TextStim(win, text = text_block, color = "white", pos = (0,0))
	msg.draw()
	win.flip()
	core.wait(display_time)

def wait_for_keypress(win, message = ''):
	'''
	Wait until subject presses spacebar.
	'''
	if message:
		present_text(win, message)
	event.waitKeys(keyList = ["space"]) # wait until subject responds

def decide_offer(trial):
	'''
	Returns text to be shown as offer depending on trial type.
	'''
	# targets
	target_self = "you"
	target_other = "the next participant"

	# trial types
	offer_reward = "Exert Effort to Win 10 Points for "
	offer_punishment = "Exert Effort to Avoid Losing 10 Points for "

	# decision tree
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
	return offer


def present_choice(win):
	'''
    Shows options (work vs. rest), waits for keyboard press
	  (left or right arrow keys)
	  and records keypress. 
    '''
	left_choice_message = visual.TextStim(win, color = "blue", pos = (-0.3, 0),
                                  text = 'Press the \nleft arrow key \nto work')
	left_choice_message.draw()
	right_choice_message = visual.TextStim(win, color = "red", pos = (+0.3, 0),
                                  text = ' Press the \nright arrow key \nto rest')
	right_choice_message.draw()
	win.flip()
	return event.waitKeys(keyList = ['left', 'right'])

def translate_choice(choice):
	'''
	Translates choice variable to string 
		('work' or 'rest').
	'''
	if ('left' in choice):
		return 'work'
	elif ('right' in choice):
		return 'rest'
	else:
		return ''

def determine_success(grip_list, MVC):
	'''
	Determine whether work trial succeeded. Success if 
	measurements remain above 70% of maximum voluntary
	contraction (MVC) for 1 second of the total time.

	Arguments:
		grip_list (lst): list of grip measurements
		MVC (float): maximum voluntary contraction

	Returns boolean: True if success, False if failure.
	'''

	n_samples = len(grip_list)

	# check to make sure have at least 1 second of data
	if n_samples < 10:
		return False
	# if have at least one second of data
	else:
		# iterate across measurements
		n_success = 0
		print('starting: ', n_success)
		for val in grip_list:
			# check the value
			if val > 0.7*MVC:
				n_success += 1
				print(n_success)
			else:
				n_success = 0
				print(n_success)
			# check number of successes
			if n_success >= 10:
				return True
			else:
				continue
		# if checked all values and did not return True
		return False


def get_squeeze(gdx_obj, sample_time, MVC):
	'''
	Samples grip strength measurements every 100ms for
	a given amount of time. If measurements remain above
	70% of maximum voluntary contraction (MVC) for 1 second, trial
	is considered successful.

	Arguments:
		gdx_obj: A Vernier dynamometer class object.
		sample_time (int): amount of time to sample
		MVC (float): participant's max grip strength
	
	Returns: tuple
		avg_grip (float): average of all sampled values for sample_time
		trial_outcome (Boolean): True if successful, False if failed.
	'''
	gdx_obj.start(100)
	measurements = []
	t0 = time()
	print('t0: ',t0)
	t = time()
	while t <= t0 + sample_time:
		measurement = gdx_obj.read()
		print(t, ': ', measurement)
		measurements.append(measurement[0])
		t = time()
	gdx_obj.stop()
	avg_grip = np.mean(measurements)
	success = determine_success(measurements, MVC)
	return (avg_grip, success)

def work_rest_segment(win, choice, gdx_obj, MVC):
	'''
	If chose to work, presents grip strength segment,
	otherwise presents "Rest".

	Returns tuple:
		avg_grip (float): mean grip strength for that trial
		success (Boolean): whether work trial succeeded
	'''
	# if choose to work
	if ('left' in choice):
		# Countdown to Grip
		present_text(win, '3')
		present_text(win, '3, 2')
		present_text(win, '3, 2, 1')

		# Grip
		present_text(win, 'SQUEEZE', 0.1)
		avg_grip, success = get_squeeze(gdx_obj, 3, MVC)
		return (avg_grip, success)

	# if choose to rest
	elif ('right' in choice):
		# rest segment
		present_text(win, 'You may rest.')

	# Anything else
	else:
		# catch all
		present_text(win, 'Please make a choice.')

def present_feedback(win, trial, choice, success):
	'''
	Present text with points lost or gained and return
		number of points.
	'''
	outcome = 'nothing'
	# if chose rest
	if ('right' in choice):
		outcome = "No points earned or lost."
		points_self = 0
		points_other = 0
	
	# if worked and succeeded
	elif ('left' in choice) & (success):
		if trial == 'self_reward':
			outcome = "+10 points for you"
			points_self = 10
			points_other = 0
		elif trial == 'self_punishment':
			outcome = "-0 points for you"
			points_self = 0
			points_other = 0
		elif trial == 'other_reward':
			outcome = '+10 points for the next participant'
			points_self = 0
			points_other = 10
		elif trial == 'other_punishment':
			outcome = '-0 points for the next participant'
			points_self = 0
			points_other = 0
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0

	# if worked and failed
	elif ('left' in choice) & (not success):
		if trial == 'self_reward':
			outcome = "+0 points for you"
			points_self = 0
			points_other = 0
		elif trial == 'self_punishment':
			outcome = "-10 points for you"
			points_self = -10
			points_other = 0
		elif trial == 'other_reward':
			outcome = '+0 points for the next participant'
			points_self = 0
			points_other = 0
		elif trial == 'other_punishment':
			outcome = '-10 points for the next participant'
			points_self = 0
			points_other = -10
		else:
			outcome = 'Warning, wrong input'
			points_self = 0
			points_other = 0
	
	present_text(win, outcome)
	return (points_self, points_other)
	
	