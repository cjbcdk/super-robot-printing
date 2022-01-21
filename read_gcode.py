from parser_helper_classes import Command # class to store commands
from parser_helper_functions import calc_new_pos # helper functions for the parser
import numpy as np # to store positions as arrays
import copy # needed to create copies of the commands when adding to list

filename = 'UMO_vase2base.gcode' # gcode filename
parsed_codes = ['M109','G90','G91','G0','G1','G28'] # store codes that are important for parsing
abs_pos_mode = True # positioning mode
layer_0_reached = False # bool variable. False until line ';LAYER:0' is reached

commands = [] # create empty list of commands
try: # start try block to catch exceptions
    reader = open(filename, 'r') # open gcode-file
    last_pos = np.zeros(3) # store last explicit definition of positions in case arguments don't specify coordinates
    for line in reader.readlines(): # read gcode file line by line
        if line == ';LAYER:0\n': # check if the first layer is reached
            layer_0_reached = True # set bool variable to True
        line = line.split(';') # split line string to ignore commands
        line = line[0] # only evaluate command before first semicolon
        if len(line)==0: # comments start with semicolon
            continue # ignore comment lines
        split_line = line.split(' ') # split string to extract command code
        code = split_line[0] # extract command code

        if code not in parsed_codes: # check if code is within important codes
            continue # if not, continue with next line

        new_command = Command() # create new object of class Command

        if code == 'G1' and not layer_0_reached: # don't print when Layer 0 was not reached yet
            code = 'G0' # set the code to G0 so no printing is performed
        new_command.code = code # save the G code command in code

        ### G1: Linear Motion
        if code in ['G0','G1']: # check if code is G0 or G1
            last_pos = calc_new_pos(last_pos, split_line[1:], abs_pos_mode) # get the goal position and save it as new last position
            new_command.goal_pos = last_pos # save goal position in new command
        ### G90: Absolute positioning
        if code == 'G90': #  check if code is G90
            abs_pos_mode = True # change positioning mode to absolute mode
            continue # G90 command should not be appended to command list
        ### G91: Relative positioning
        if code == 'G91': #  check if code is G91
            abs_pos_mode = False # change positioning mode to relative mode
            continue # G91 command should not be appended to command list
        ### G28: Go to home position
        if code == 'G28': # check if code is G28
            new_command.code = 'G0' # treat G28 as G0 (move linear without extrusion)
            last_pos = np.zeros(3) # update last position variable
            new_command.goal_pos = last_pos # save as goal position
        ### M109: heat and wait for Temp (no args)
        # no action required
        commands.append(copy.deepcopy(new_command)) # add the new command to the list of commands
finally: # code to be executed after try block
    print('Parsing of gcode successful.') # confirm successful parsing
    reader.close() # close .gcode file