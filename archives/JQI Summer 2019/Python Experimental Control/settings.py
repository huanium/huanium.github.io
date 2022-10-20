# this script defines some of the global variables

def init():
    global new_time_points
    global old_time_points
    global default_num_pts
    global event
    global values
    global sequence
    global instructions
    global ana_00
    global ana_01
    global ana_02
    global ana_03
    global ana_04
    global window
    global inserted_values
    global inserted
    global ramped
    global switch
    global ana_05
    global items_per_row
    global other_items
    global digital_channels
    global ignore
    global scan_parameters
    global file_name
    global save_as
    global logo_scaled_by

    logo_scaled_by = 2
    save_as = 'exp_sequence.csv'
    file_name = 'exp_sequence.csv' # this is the default value. Might get changed
    # whether to ignore a warning. (True/False)
    ignore = True
    # number of digital channels
    digital_channels = 8
    # number of items per time point
    items_per_row = 16
    # number of other items on the menu
    other_items = 33
    window = None
    window_view = None
    new_time_points = 10
    old_time_points = 10
    new_time_points_view = 10
    old_time_points_view = 10
    default_num_pts = 5
    event = ''
    values = {}
    event_view = ''
    values_view = {}
    inserted_values = {}
    sequence = {}
    instructions = []
    ana_00 = []
    ana_01 = []
    ana_02 = []
    ana_03 = []
    ana_04 = []
    ana_05 = []
    inserted = False
    ramped = False
    switch = []
    deleted = False
