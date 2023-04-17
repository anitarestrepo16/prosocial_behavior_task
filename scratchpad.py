import numpy as np

from utils.ui import (
    fixation_cross
)

#### Text String Objects ####
# targets
target_self = "You"
target_other = "Next Participant"
targets = [target_self, target_other]
# trial types
offer_reward = "Exert Effort to Win 10 Points for "
offer_punishment = "Exert Effort to Avoid Losing 10 Points for "
offers = [offer_reward, offer_punishment]
# choices
work = "Work"
rest = "Rest"
choices = [work, rest]
# outcomes
win_reward = "+10 Points for "
win_punishment = "-0 Points for "
lose_reward = "-0 Points for "
lose_punishment = "-10 Points for "
outcomes = [win_reward, win_punishment, lose_reward, lose_punishment]
# grip strength effort
go = "SQUEEZE"

# Hardware
win = visual.Window([800,600], monitor="testMonitor", units="deg")

###### Trial Segments #######
# Offer
offer_message = visual.TextStim(win, pos = [0, +3], text = offers[0] + targets[0])
offer_message.draw()
win.flip()
core.wait(1)

# Fixation
fixation_cross = visual.TextStim(win, pos = [0, +3], text = '+')
fixation_cross.draw()
win.flip()
core.wait(1)

# Choice
left_choice_message = visual.TextStim(win, pos = [-3, +3],
                                  text = 'Press the \nleft arrow key \nto ' + choices[0])
left_choice_message.draw()
right_choice_message = visual.TextStim(win, pos = [+3, +3],
                                  text = ' Press the \nright arrow key \nto ' + choices[1])
right_choice_message.draw()
win.flip()
choice = event.waitKeys()
print(choice)

# Fixation
fixation_cross = visual.TextStim(win, pos = [0, +3], text = '+')
fixation_cross.draw()
win.flip()
core.wait(1)

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
    grip_message = visual.TextStim(win, pos = [0, +3], text = go)
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

# Fixation
fixation_cross = visual.TextStim(win, pos = [0, +3], text = '+')
fixation_cross.draw()
win.flip()
core.wait(1)

# Feedback
feedback_message = visual.TextStim(win, pos = [0, +3], text = outcomes[0] + targets[0])
feedback_message.draw()
win.flip()
core.wait(0.5)

# Fixation
fixation_cross = visual.TextStim(win, pos = [0, +3], text = '+')
fixation_cross.draw()
win.flip()
core.wait(1)