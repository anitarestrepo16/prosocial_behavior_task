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

########################
# Maximum Voluntary Contraction (MVC)
########################

# Instructions  


dynamo.draw()
txt = '''
First we're going to measure your maximum grip strength using
 the grip strength sensor (pictured below). \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)

grip_right.draw()
txt = '''
This is the way you should hold the grip strength sensor. 
Make sure your fingers are wrapped tightly around it like
in the picture. \n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)
str1 = visual.TextStim(win, "work to", color = 'white',
			       pos = (0, 0.6))
type_txt = visual.TextStim(win, "EARN", color = 'pink',
			       pos = (0, 0.4))
str2 = visual.TextStim(win, "10 points for", color = 'white',
			       pos = (0, 0.2))
target_txt = visual.TextStim(win, "YOURSELF", color = 'gold',
			       pos = (0, 0))
str1.draw()
type_txt.draw()
str2.draw()
target_txt.draw()
win.flip()

wait_for_keypress(win, "")