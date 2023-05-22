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
    get_MVC
)
from utils.write import CSVWriter
from utils.triggerer import Triggerer
from utils.gdx import gdx

# initialize some things
parport = Triggerer(0)
grip = gdx.gdx()
grip.open(connection = 'usb', device_to_open = 'GDX-HD 15400221')
grip.select_sensors([1])
parport.set_trigger_labels(['MVC_start', 'MVC_end', 'baseline_start', 'baseline_end', 'show_offer', 'make_choice', 'work_rest', 'feedback'])
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
log = CSVWriter(subj_num)
np.random.seed(subj_num)
points_self = 0
points_other = 0
trial_num = 1
MVC_time = 3
baseline_time = 3

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


win = visual.Window(
	size = (800, 600),
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)

t1 = time()
ANCHOR_Y = 0
MVC = 1
demark = ANCHOR_Y + MVC*0.7
demark_bar = visual.Line(win)
demark_bar.start = (-0.3, demark)
demark_bar.end = (0.3, demark)
demark_bar.color = 'red'
demark_bar.draw()
win.flip()

current_bar = visual.rect.Rect(win, pos = (0, ANCHOR_Y), anchor = 'bottom')
current_bar.color = 'white'

grip.start(100)
measurements = []
t0 = time()
print('t0: ',t0)
t = time()
while t <= t0 + 3:
	measurement = grip.read()
	print(t, ': ', measurement)
	current_bar.height = measurement
	demark_bar.draw()
	current_bar.draw()
	win.flip()
	measurements.append(measurement[0])
	t = time()
grip.stop()


grip.close()
t2 = time()
