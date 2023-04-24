import numpy as np
from collections import OrderedDict
from psychopy import visual, event
from time import time

from utils.ui import (
    fixation_cross,
    present_text,
    wait_for_keypress,
    present_choice,
    work_rest_segment
)



# initialize some things
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
#log = TSVWriter(subj_num)
np.random.seed(subj_num)
# targets
target_self = "You"
target_other = "Next Participant"
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

# specify block design -- n_trials, [target, trial_type]
BLOCKS = OrderedDict()
BLOCKS['self_reward'] = (25, ['self', 'reward']) 
BLOCKS['self_punishment'] = (25, ['self', 'punishment']) 
BLOCKS['other_reward'] = (25, ['other', 'reward'])
BLOCKS['random2'] = (25, ['other', 'punishment'])
########## still need to figure out how to randomize trial order

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
for block_code in BLOCKS:

	t2 = time()
	print("\nBeginning %s block\n"%block_code)
	print("It's been %d minutes since the experiment started."%((t2 - t1)/60))
	trial_info = BLOCKS[block_code]
	n_trials = trial_info[0]

	for trial in range(n_trials):

		# decide what to do this trial
		### need to figure out how to randomize what shows up in this part and save data
		
		offer = offers[0] + targets[0] 


		# keep experimenter in the loop via console
		stdout.write("\rTrial {0:03d}".format(trial) + "/%d"%n_trials)
		stdout.flush()

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

		# fixation (ITI)
		fixation_cross(win)


		wait_for_keypress(win, message = 'Press spacebar to continue.')
		
		
		start_t = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		display(win, sentence) # flips screen
		marker.send(trial + 1) # mark with trial number, 1-indexed
		wait_for_keypress(win)
		end_t = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		marker.send(127) # end trial
		detected_delay = ask_whether_delay(win)
		resp_tag = 125 if detected_delay else 126
		marker.send(resp_tag)
		log.write(
			block_code,
			trial + 1,
			delay,
			sentence,
			detected_delay,
			start_t,
			end_t
		)

marker.close()
audio.stop()
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
