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

def wait_for_choice():
	'''
    Wait for keyboard press (left or right arrow keys)
        and records keypress. 
    '''
	return event.waitKeys(['left', 'right'])