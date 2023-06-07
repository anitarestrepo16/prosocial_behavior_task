import numpy as np
from psychopy import visual, event
from time import time
import random

from utils.ui import (
    draw_grip
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
	size = (800, 600),
	screen = -1,
	units = "norm",
	fullscr = False,
	pos = (0, 0),
	allowGUI = False
	)
ANCHOR_Y = -0.5

draw_grip(win, -0.5, 720, 1200)
draw_grip(win, -0.5, 620, 1200)

draw_grip(win, 0, 720, 1200)
draw_grip(win, 0, 620, 1200)