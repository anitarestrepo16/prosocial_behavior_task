import numpy as np
from collections import OrderedDict
from psychopy import visual, event
from time import time

from utils.ui import (
    fixation_cross,
    wait_for_keypress,
    wait_for_choice
)

# specify block design
BLOCKS = OrderedDict()
BLOCKS['baseline'] = (20, 0) # n_trials, milliseconds added delay
BLOCKS['random1'] = (50, None) # None denotes random delay
BLOCKS['adaption'] = (80, 200)
BLOCKS['random2'] = (50, None)

# initialize some things
subj_num = input("Enter subject number: ")
subj_num = int(subj_num)
#log = TSVWriter(subj_num)
np.random.seed(subj_num)

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
	des = BLOCKS[block_code]
	n_trials = des[0]

	for trial in range(n_trials):

		# decide what to do this trial
		delay = np.random.randint(0, 250) if des[1] is None else des[1]
		sentence = sentences.pop(0)

		# keep experimenter in the loop via console
		stdout.write("\rTrial {0:03d}".format(trial) + "/%d"%n_trials)
		stdout.flush()

		# now actually run the trial
		wait_for_keypress(win, message = 'Press spacebar to continue.')
		audio.set_delay(delay)
		fixation_cross(win)
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
