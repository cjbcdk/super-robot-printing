import numpy as np # to define position vector
import re # to check command arguments
from parser_helper_classes import Command # class to store commands

arg_r = re.compile(r"[XYZ][\+\-]?\d+(\.\d*)?") # initialize pattern for command arguments

def extract_pos_from_split_line(split_line): # used to extract the goal position from a command line
    pos = np.zeros(3) # init position vector
    pos_valid = np.zeros(3, dtype=np.bool_) # init logical vector to track which coordinates have been read in
    coord_dict = {'X':0, 'Y':1, 'Z':2} # dictionary to index position vector
    for word in split_line: # do for every argument
        if arg_r.match(word) is not None: # check if arguments matches the pattern
            pos[coord_dict[word[0]]] = float(word[1:]) # set respective coordinate to argument
            pos_valid[coord_dict[word[0]]] = True # set logical vector to true
    return pos, pos_valid # return variables

def calc_new_pos(last_pos, line, abs_pos_mode): # used to calculate the new position from the last position and the command line
    pos_cmd, pos_cmd_valid = extract_pos_from_split_line(line) # extract the position from the command line
    new_pos = np.zeros(3) # init new pose to be calculated
    if abs_pos_mode: # check if absolute or relative positioning is activated
        last_pos[pos_cmd_valid] = 0 # if absolute positioning is on: all values of the old position, which have not been set by command, have to be ignored (set to zero)
    new_pos = last_pos + pos_cmd # combine last position and goal position in command
    return new_pos # return the calculated position