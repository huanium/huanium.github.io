# this script defines some of the global variables

def init():
    global new_time_points
    global old_time_points
    global default_num_pts
    global event
    global values
    global sequence
    global instructions
    global AH
    global Trap
    global Repump
    global aom
    global vco
    global window
    global inserted_values
    global inserted
    global ramped
    global switch
    global vca
    global items_per_row
    global other_items
    global digital_channels
    global ignore
    global scan_parameters
    global file_name
    global save_as

    save_as = 'exp_sequence.csv'
    file_name = 'exp_sequence.csv' # this is the default value. Might get changed
    # whether to ignore a warning. (True/False)
    ignore = True
    # number of digital channels
    digital_channels = 8
    # number of items per time point
    items_per_row = 16
    # number of other items on the menu
    other_items = 19
    window = None
    new_time_points = 10
    old_time_points = 10
    default_num_pts = 5
    event = ''
    values = {}
    inserted_values = {}
    sequence = {}
    instructions = []
    AH = []
    Trap = []
    Repump = []
    aom = []
    vco = []
    vca = []
    inserted = False
    ramped = False
    switch = []
    deleted = False
