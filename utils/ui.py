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

def present_text(win, text_block, text_col = 'white', display_time = 1, position = (0, 0)):
	'''
	Displays a block of text on the screen.
	'''
	msg = visual.TextStim(win, text = text_block, color = text_col, pos = position)
	msg.draw()
	win.flip()
	core.wait(display_time)

def wait_for_keypress(win, message = ''):
	'''
	Wait until subject presses spacebar.
	'''
	if message:
		present_text(win = win, text_block = message, position = (0, 0.2))
	event.waitKeys(keyList = ["space"]) # wait until subject responds

def decide_offer(trial):
	'''
	Returns text to be shown as offer depending on trial type.
	'''
	# targets
	target_self = "YOURSELF"
	target_other = "THE NEXT PARTICIPANT"

	# trial types
	offer_reward = "EARN"
	offer_punishment = "AVOID LOSING"

	# decision tree
	if trial == 'self_reward':
		offer = (offer_reward, target_self)
	elif trial == 'self_punishment':
		offer = (offer_punishment, target_self)
	elif trial == 'other_reward':
		offer = (offer_reward, target_other)
	elif trial == 'other_punishment':
		offer = (offer_punishment, target_other)
	else:
		offer = ("Warning", "wrong input")
	return offer

def present_offer(win, type, target, display_time):
	'''
	Present offer with key words color-coded.
	'''
	str1 = visual.TextStim(win, "Offer: Work to", color = 'white',
			       pos = (0, 0.6))
	if type == 'EARN':
		type_col = 'pink'
	elif type == 'AVOID LOSING':
		type_col = 'forestgreen'
	type_txt = visual.TextStim(win, type, color = type_col,
					pos = (0, 0.4))
	str2 = visual.TextStim(win, "10 points for", color = 'white',
					pos = (0, 0.2))
	if target == 'YOURSELF':
		target_col = 'gold'
	elif target == 'THE NEXT PARTICIPANT':
		target_col = 'purple'
	target_txt = visual.TextStim(win, target, color = target_col,
					pos = (0, 0))
	str1.draw()
	type_txt.draw()
	str2.draw()
	target_txt.draw()
	win.flip()
	core.wait(display_time)

def present_choice(win):
	'''
    Shows options (work vs. rest), waits for keyboard press
	  (left or right arrow keys)
	  and records keypress. 
    '''
	left_choice_message = visual.TextStim(win, color = "SteelBlue", pos = (-0.3, 0),
                                  text = 'WORK \n <--')
	left_choice_message.draw()
	right_choice_message = visual.TextStim(win, color = "Chocolate", pos = (+0.3, 0),
                                  text = 'REST \n -->')
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

def draw_grip(win, y_anchor, force, MVC):
	'''
	Draw a target force line and a rectangle where the
	  height is the force exerted.

	Arguments:
		win: the psychopy window to draw to
		y_anchor (float): the vertical height to anchor the bottom of the rect
		force (float): the grip strength force exerted
		MVC (float): max voluntary contraction
	'''
	# rescale newtons to pixels
	MVC_pix = MVC/MVC
	force_pix = force/MVC
	# set target bar
	target = y_anchor + MVC_pix*0.7 # anchor plus 70% of MVC
	target_bar = visual.Line(win)
	target_bar.start = (-0.3, target)
	target_bar.end = (0.3, target)
	target_bar.color = 'red'
	# set target text
	target_txt = visual.TextStim(win, "<-- TARGET", color = 'red',
			       pos = (0.3, target), alignText = 'left', anchorHoriz = 'left')
	# set force bar
	force_bar = visual.rect.Rect(win, pos = (0, y_anchor), anchor = 'bottom')
	force_bar.color = 'white'
	force_bar.height = force_pix

	# draw
	target_bar.draw()
	target_txt.draw()
	force_bar.draw()
	win.flip()
	
def get_squeeze(gdx_obj, sample_time):
	'''
	Samples grip strength measurements every 100ms for
	a given amount of time. 

	Arguments:
		gdx_obj: A Vernier dynamometer class object.
		sample_time (int): amount of time to sample
	
	Returns: list of all sampled measurements (in Newtons). 
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
	return measurements

def get_squeeze_and_viz(gdx_obj, sample_time, win, y_anchor, MVC):
	'''
	Samples grip strength measurements every 100ms for
	a given amount of time and visualizes strength at each sample.

	Arguments:
		gdx_obj: A Vernier dynamometer class object.
		sample_time (int): amount of time to sample
		win: the psychopy window to draw to
		y_anchor (float): the vertical height to anchor the bottom of the rect
		MVC (float): max voluntary contraction
	
	Returns: list of all sampled measurements (in Newtons). 
	'''
	gdx_obj.start(100)
	measurements = []
	t0 = time()
	print('t0: ',t0)
	t = time()
	while t <= t0 + sample_time:
		measurement = gdx_obj.read()
		print(t, ': ', measurement)
		draw_grip(win, y_anchor, measurement[0], MVC)
		measurements.append(measurement[0])
		t = time()
	gdx_obj.stop()
	present_text(win, 'STOP', 'red', 0.5)
	return measurements

def get_MVC(win, gdx_obj, sample_time):
	'''
	Obtain participant's maximum vountary contraction (MVC).

	Arguments:
		gdx_obj: A Vernier dynamometer class object.
		sample_time (int): amount of time to sample

	Returns: MVC (float)
	'''
	# Countdown to Grip
	present_text(win, '3')
	present_text(win, '3, 2')
	present_text(win, '3, 2, 1')

	# Grip
	present_text(win, 'SQUEEZE', 'white', 0.1)
	measurements = get_squeeze(gdx_obj, sample_time)
	present_text(win, 'STOP', 'red', 0.5)
	return np.max(measurements)


def grip_segment(gdx_obj, sample_time, MVC, win, y_anchor):
	'''
	Samples grip strength measurements every 100ms for
	a given amount of time. If measurements remain above
	70% of maximum voluntary contraction (MVC) for 1 second, trial
	is considered successful.

	Arguments:
		gdx_obj: A Vernier dynamometer class object.
		sample_time (int): amount of time to sample
		MVC (float): participant's max grip strength
		win: the psychopy window to draw to
		y_anchor (float): the vertical height to anchor the bottom of the rect
	
	Returns: tuple
		avg_grip (float): average of all sampled values for sample_time
		trial_outcome (Boolean): True if successful, False if failed.
	'''
	measurements = get_squeeze_and_viz(gdx_obj, sample_time, win, y_anchor, MVC)
	avg_grip = np.mean(measurements)
	success = determine_success(measurements, MVC)
	return (avg_grip, success)

def work_rest_segment(win, choice, gdx_obj, MVC, y_anchor):
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
		present_text(win, 'SQUEEZE', 'white', 0.1)
		avg_grip, success = grip_segment(gdx_obj, 3, MVC, win, y_anchor) # sample 3s
		return (avg_grip, success)

	# if choose to rest
	elif ('right' in choice):
		# rest segment
		present_text(win, 'You may rest.')
		return (-99, False)

	# Anything else
	else:
		# catch all
		present_text(win, 'Please make a choice.')

def present_feedback(win, trial, choice, success, display_time):
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
	core.wait(display_time)
	return (points_self, points_other)
	
def fatigue_segment(win):
	'''
	Present a slider for subjects to rate fatigue from
		0 to 100 and return the rating.

	Arguments:
		win: psychopy window to present stimuli on
	
	Returns fatigue rating (int). 
	'''
	# create rating scale
	fatigue_scale = visual.RatingScale(win, low = 0, high = 100,
				    scale = None, 
					tickMarks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
					marker = 'slider', markerStart = 50,
					markerColor = 'DarkRed', stretch = 2)
	# create instruction message
	msg = visual.TextStim(win, 
			text = "Rate your current fatigue from 0 to 100:",
			color = "white", pos = (0,0))
		
	# draw and collect response
	while fatigue_scale.noResponse:
		msg.draw()
		fatigue_scale.draw()
		win.flip()
	
	return fatigue_scale.getRating()