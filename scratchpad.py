import numpy as np
from psychopy import visual, event, monitors
from time import time
import random

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    decide_offer,
    present_offer,
    present_choice,
    translate_choice,
    work_rest_segment,
    present_feedback,
    get_MVC,
    determine_MVC,
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

# practice trials
practice_trials = [
	'self_reward',
	'other_reward',
	'self_punishment',
	'other_punishment'
]

# make trials list
trials_per_type = 25 # 25
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
	size = (1920, 1080),
	color = (0, 0, 0),
	colorSpace = 'rgb255',
	screen = -1,
	units = "norm",
	fullscr = False, 
	#pos = (0, 0),
	allowGUI = False
	)
ANCHOR_Y = -0.5
MVC_TIME = 3 # 3s
BASELINE_TIME = 300 # 5 min (300s)
OFFER_TIME = 3.5 # 3.5s
FEEDBACK_TIME = 0.5 # 0.5s
BREAK_TIME = 30 # 30s

dynamo = visual.ImageStim(win, 'image_stim/Go_Direct_Dynomometer.jpg', pos = (0, -0.5), size = (.51, .4))
grip_right = visual.ImageStim(win, 'image_stim/grip_right.jpg', pos = (0, 0), size = (.7, .5))
choice_img = visual.ImageStim(win, 'image_stim/choice.png', pos = (0, -0.2), size = (.8, .45))
rest_points = visual.ImageStim(win, 'image_stim/rest_points.PNG', pos = (-.3, -.1), size = (.72, .55))
work_points = visual.ImageStim(win, 'image_stim/work_points.PNG', pos = (.3, -.1), size = (.72, .55))
squeeze_success = visual.ImageStim(win, 'image_stim/squeeze_success.png', pos = (0, -0.1), size = (.72, .55))
squeeze_fail = visual.ImageStim(win, 'image_stim/squeeze_fail.png', pos = (0, -0.1), size = (.72, .55))
work_earn_success = visual.ImageStim(win, 'image_stim/ex_work_earn_success.png', pos = (0, -0.1), size = (.72, .55))
work_earn_failure = visual.ImageStim(win, 'image_stim/ex_work_earn_fail.png', pos = (0, -0.1), size = (.72, .55))
work_avoid_success = visual.ImageStim(win, 'image_stim/ex_work_avoid_success.png', pos = (0, -0.1), size = (.72, .55))
work_avoid_failure = visual.ImageStim(win, 'image_stim/ex_work_avoid_fail.png', pos = (0, -0.1), size = (.72, .55))
rest_earn = visual.ImageStim(win, 'image_stim/ex_rest_earn.png', pos = (0, -0.1), size = (.72, .55))
rest_avoid = visual.ImageStim(win, 'image_stim/ex_rest_avoid.png', pos = (0, -0.1), size = (.72, .55))
arrow_rest_earn = visual.ImageStim(win, 'image_stim/rest_earn_only.png', pos = (-.3, -.1), size = (.72, .55))
arrow_work_earn = visual.ImageStim(win, 'image_stim/arrow_work_earn.png', pos = (.3, -.1), size = (.72, .55))
arrow_work_avoid = visual.ImageStim(win, 'image_stim/arrow_work_avoid.png', pos = (.3, -.1), size = (.72, .55))


########################
# Maximum Voluntary Contraction (MVC)
########################
print("Starting Instructions!")
mvc = 100

choice_img.draw()
txt = '''
\n
\n
To choose WORK, you press the left arrow key. To choose REST, 
you press the right arrow key. You have 3 seconds to make your choice!\n
\n
\n
\n
Press the spacebar to continue.
'''
wait_for_keypress(win, txt)



# Practice
print("Starting Practice Trials!")
for trial in practice_trials:
	# offer
	type, target = decide_offer(trial)
	present_offer(win, type, target, OFFER_TIME)
	# fixation
	fixation_cross(win)
	# choice
	choice, choice_RT = present_choice(win)
	print(choice, str(choice_RT))
	# fixation
	fixation_cross(win)
	# work/rest
	avg_grip, max_grip, min_grip, success = work_rest_segment(win, choice, grip, mvc, ANCHOR_Y)
	# fixation
	fixation_cross(win)
	# feeback
	points = present_feedback(win, trial, choice, success, FEEDBACK_TIME)
	# fixation (ITI)
	fixation_cross(win)



# Run Prosocial Behavior Task
print("Starting Main Task!")


# cycle through blocks
for block in blocks:

	for trial in block:

		print("Starting trial " + str(trial_num))
		# decide what to offer this trial
		type, target = decide_offer(trial)
		# show offer
		parport.send_trigger('show_offer')
		present_offer(win, type, target, OFFER_TIME)
		# fixation
		fixation_cross(win)
		# choice
		parport.send_trigger('make_choice')
		choice, choice_RT = present_choice(win)
		# fixation
		fixation_cross(win)
		# work/rest
		parport.send_trigger('work_rest')
		avg_grip, max_grip, min_grip, success = work_rest_segment(win, choice, grip, mvc, ANCHOR_Y)
		# fixation
		fixation_cross(win)
		# feeback
		parport.send_trigger('feedback')
		points = present_feedback(win, trial, choice, success, FEEDBACK_TIME)
		# keep track of point changes
		points_self += points[0]
		points_other += points[1]
		# fixation (ITI)
		fixation_cross(win)

		# save data
		choice = translate_choice(choice)
		print("Participant Success: " + str(success))
		print("Participant chose " + choice + " after " + str(choice_RT) + " seconds")
		trial_log.write(
			block_num,
			trial_num,
			trial,
			choice,
			choice_RT,
			avg_grip, 
			max_grip,
			min_grip,
			success,
			points[0],
			points[1]
		)
		trial_num += 1
		# trial end

	# fatigue rating
	print("Fatigue starting!")
	parport.send_trigger('fatigue_start')
	fatigue_rating = fatigue_segment(win)
	parport.send_trigger('fatigue_end')
	print("Fatigue ended.")
	block_log.write(block_num, fatigue_rating)

	# short break
	if block_num < 4:
		print("Starting break!")
		present_text(win, 'You can take a short break now.', 'white', BREAK_TIME)
		print("Break ended!")
		wait_for_keypress(win, 'Press the spacebar to continue the task.')
		block_num += 1
	# block end

grip.close()
t2 = time()
print('Task Complete.')
print('The task took %d minutes.'%((t2 - t1)/60))
print('Participant earned %d points for themselves.'%(points_self))
print('Participant earned %d dollars for themselves.'%(points_self/20))
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
