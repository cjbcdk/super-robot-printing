import numpy as np # necessary to save position as a numpy array

class Command: # create new class named 'Command'
    code = '' # stores G code command (G0, G1, ...)
    goal_pos = np.empty((3,1)) # stores the goal position for the G0 and G1 commands