from psychopy import visual, core, event
from psychopy.tools.filetools import fromFile, toFile
import numpy as np
import random

def fixation_cross(win):
	'''
	Displays a fixation cross for a random amount of time between
	200 and 400 milliseconds.
	'''
	fixation = visual.TextStim(win, text = '+', color = "white", pos = (0,0))
	fixation.draw()
	win.flip()
	core.wait(np.random.uniform(.2, .4))

def present_text(win, text_block):
	'''
	Displays a block of text on the screen.
	'''
	msg = visual.TextStim(win, text = text_block, color = "white", pos = (0,0))
	msg.draw()
	win.flip()

def wait_for_keypress(win, message = ''):
	'''
	Wait until subject presses spacebar.
	'''
	if message:
		present_text(win, message)
	event.waitKeys(keyList = ["space"]) # wait until subject responds

def present_choice(win):
	'''
    Shows options (work vs. rest), waits for keyboard press
	  (left or right arrow keys)
	  and records keypress. 
    '''
	choices = ['Work', 'Rest']
	left_choice_message = visual.TextStim(win, pos = [-3, +3],
                                  text = 'Press the \nleft arrow key \nto ' + choices[0])
	left_choice_message.draw()
	right_choice_message = visual.TextStim(win, pos = [+3, +3],
                                  text = ' Press the \nright arrow key \nto ' + choices[1])
	right_choice_message.draw()
	win.flip()
	return event.waitKeys(['left', 'right'])

def work_rest_segment(win, choice):
	'''
	If chose to work, presents  grip strength segment,
	otherwise presents "Rest".
	'''
	# if choose to work
	if 'left' in choice:
		# Countdown to Grip
		countdown_message = visual.TextStim(win, pos = [0, +3], text = '3')
		countdown_message.draw()
		win.flip()
		core.wait(0.5)
		countdown_message.text = '3, 2'
		countdown_message.draw()
		win.flip()
		core.wait(0.5)
		countdown_message.text = '3, 2, 1'
		countdown_message.draw()
		win.flip()
		core.wait(0.5)

		# Grip
		grip_message = visual.TextStim(win, pos = [0, +3], text = "SQUEEZE")
		grip_message.draw()
		win.flip()
		core.wait(1)

	# if choose to rest
	elif 'right' in choice:
		# rest segment
		rest_message = visual.TextStim(win, pos = [0, +3], text = 'You may rest.')
		rest_message.draw()
		win.flip()
		core.wait(1)

	# Anything else
	else:
		# catch all
		error_message = visual.TextStim(win, pos = [0, +3], text = 'Please make a choice')
		error_message.draw()
		win.flip()
		core.wait(1)

def present_feedback(win, trial, choice, success):
	# if chose rest
	if 'right' in choice:
		present_text(win, "No points earned or lost.")
	
	# if worked and succeeded
	elif 'left' in choice & success:
		if trial == 'self_reward':
			outcome = offer_reward + target_self
		elif trial == 'self_punishment':
			offer = offer_punishment + target_self
		elif trial == 'other_reward':
			offer = offer_reward + target_other
		elif trial == 'other_punishment':
			offer = offer_punishment + target_other
		else:
			offer = "Warning, wrong input"

		present_text(win, outcome)
	
	# if wo