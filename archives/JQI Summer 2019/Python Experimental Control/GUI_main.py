import PySimpleGUI as sg
import GUI_functions as GUI
import settings
import numpy as np
import csv
import pickle
import PCI_control as PCI




def print_sequence(sequence):
    # this function prints sequence
    for key , val in sorted(sequence.items()):
        print(str(key)+"\t", str(val))












def save_sequence(values):
    # saves the sequence, by assigning the values dictionary
    # to the sequence variable in settings.py
    settings.sequence = settings.values.copy()















def record_sequence(values, save_as = 'exp_sequence.csv'):
    # this function writes the experimental sequence to a csv file
    # write a csv version of the exp_sequence for inspection
    # save_as the file name the sequence is going to be saved as
    # if not specified, it will be exp_sequence.csv
    with open(save_as, 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, dialect = 'excel')
        for k,v in values.items():
            w.writerow([k,v])
    return












def record_sequence_and_check_errors(values, file_name = 'exp_sequence.csv'):
    # this function writes the experimental sequence to a csv file
    # write a csv version of the exp_sequence for inspection
    with open(file_name, 'w') as f:  # Just use 'w' mode in 3.x
        w = csv.writer(f, dialect = 'excel')
        for k,v in values.items():
            w.writerow([k,v])
    # compare delays and sampling rate to see if compatible
    # if delay is less than time resolution then creates popup warning
    time_res = 1/float(values['_rate_'])
    num_events = int((len(values) - settings.other_items)/settings.items_per_row)
    for i in range(num_events):
        if float(values['_delay_' + str(i) + '_']) < time_res:
            # sg.Popup('Warning!', 'Delay is less than time resolution! \n OK to ignore.')
            win1 = sg.Window('Warning',
                    [[sg.Text('Delay is less than time resolution! \n OK to ignore or Cancel')], [sg.OK(), sg.Cancel()] ])
            e1,v1 = win1.Read()
            while True:
                if e1 is None:
                    break
                else:
                    print(e1)
                if e1 == 'OK':
                    settings.ignore = True
                    break
                elif e1 == 'Cancel':
                    settings.ignore = False
                    break
            win1.Close()
            break
            return

        if float(values['_delay_' + str(i) + '_']) > 1e4*time_res:
            # sg.Popup('Warning!', 'Consider reducing the sampling rate. \n This might take a while to load! \n OK to ignore, but be patient,. it will load eventually.')
            win2 = sg.Window('Warning',
                [[sg.Text('Consider reducing the sampling rate. \n This might take a while to load! \n OK to ignore, but please be patient.')], [sg.OK(), sg.Cancel()] ])
            e2, v2 = win2.Read()
            while True:
                if e2 is None:
                    break
                else:
                    print(e2)
                if e2 == 'OK':
                    settings.ignore = True
                    break
                elif e2 == 'Cancel':
                    settings.ignore = False
                    break
            win2.Close()
            break
            return
    return








def read_sequence(file_name = 'exp_sequence.csv'):
    # this function reads an experimental sequence
    # and gives to py to create new window
    # with old specifications from last time
    # input: none. It just reads the exp_sequence.csv in the folder
    # output: a dictionary that will be fed to window creation
    # defualt file name is 'exp_sequence.csv'
    #
    sequence = {}
    with open(file_name) as fp:

        for line in fp:
            line = line.rstrip("\n")
            pair = line.split(',')
            if pair != ['']:
                sequence.update({pair[0]: pair[1]})

    settings.sequence = sequence.copy() # assigns this new sequence to settings
    return settings.sequence













def update_sequence(file_name = 'exp_sequence.csv'):
    # this function updates the experimental specifications
    # changes as applied throughout
    save_sequence(settings.values)
    record_sequence(settings.values, file_name)
    read_sequence(file_name)
    print('Sequence updated!')
    return











def update_sequence_and_check_errors(file_name = 'exp_sequence.csv'):
    # this function updates the experimental specifications
    # changes as applied throughout
    save_sequence(settings.values)
    record_sequence_and_check_errors(settings.values)
    read_sequence(file_name)
    return













def sequence_to_instructions_spin(file_name = 'exp_sequence.csv'):

    # this function takes the sequence, which is a dictionary,
    # and turns it into instructions for the next start-up
    # essentially this saves the exp specs
    # input: N/A
    # output: settings.instructions which is a global var

    read_sequence(file_name)

    settings.instructions  = []
    spin = int(settings.sequence['_spin_'])
    iter = str(settings.sequence['_iter_'])
    num_rows = int((len(settings.sequence) - settings.other_items)/settings.items_per_row)

    if spin <= num_rows: # new number of rows is less than before
        for row in range(spin):
            row_switch = ['']*settings.digital_channels
            mode = settings.sequence[str('_mode_'+str(row)+'_')]
            delay = settings.sequence[str('_delay_'+str(row)+'_')]
            for col in range(settings.digital_channels):
                row_switch[col] = settings.sequence[str('_switch_' + str(row) + '_' + str(col) + '_' )]
            # step = settings.sequence[str('_step_'+str(row)+'_')]
            ana_00 = settings.sequence[str('_ana_00_'+str(row)+'_')]
            ana_01 = settings.sequence[str('_ana_01_'+str(row)+'_')]
            ana_02 = settings.sequence[str('_ana_02_'+str(row)+'_')]
            ana_03 = settings.sequence[str('_ana_03_'+str(row)+'_')]
            ana_04 = settings.sequence[str('_ana_04_'+str(row)+'_')]
            ana_05 = settings.sequence[str('_ana_05_'+str(row)+'_')]

            row_specs = [mode, delay, row_switch, ana_00, ana_01, ana_02, ana_03, ana_04, ana_05]
            settings.instructions.append(row_specs)

        return settings.instructions

    else: # do the same thing up to the old points, then set new rows to last row
        for row in range(num_rows):
            row_switch = ['']*settings.digital_channels
            mode = settings.sequence[str('_mode_'+str(row)+'_')]
            delay = settings.sequence[str('_delay_'+str(row)+'_')]
            for col in range(settings.digital_channels):
                row_switch[col] = settings.sequence[str('_switch_' + str(row) + '_' + str(col) + '_' )]
            # step = settings.sequence[str('_step_'+str(row)+'_')]
            ana_00 = settings.sequence[str('_ana_00_'+str(row)+'_')]
            ana_01 = settings.sequence[str('_ana_01_'+str(row)+'_')]
            ana_02 = settings.sequence[str('_ana_02_'+str(row)+'_')]
            ana_03= settings.sequence[str('_ana_03_'+str(row)+'_')]
            ana_04 = settings.sequence[str('_ana_04_'+str(row)+'_')]
            ana_05 = settings.sequence[str('_ana_05_'+str(row)+'_')]

            row_specs = [mode, delay, row_switch, ana_00, ana_01, ana_02, ana_03, ana_04, ana_05]
            settings.instructions.append(row_specs)

        for new_row in range(spin - num_rows):
            new_row_specs = settings.instructions[-1] # just copying the last row
            settings.instructions.append(new_row_specs)
        # print(settings.instructions)
        return settings.instructions















def insert(location):
    # this function inserts a time point into the program
    # - updates the values (dictionary)
    # - updates the .csv file by changing the number of spinners
    # - copying the row right before it and add this row
    # - then shifting everything after by one time point.
    # - then restarting the window.
    # input: the location of insertion

    read_sequence()
    settings.values['_spin_'] = str(int(settings.values['_spin_']) + 1) # spinners increase by 1.
    spin = int(settings.values['_spin_']) # this is the location of the last row
    iter = str(settings.values['_iter_'])
    num_rows = int((len(settings.values) - settings.other_items)/settings.items_per_row)

    # adding the last row
    settings.values['_mode_' + str(spin-1) + '_'] = '-Select-'
    settings.values['_delay_' + str(spin-1) + '_'] = '0.0005'
    settings.values['_switch_' + str(spin-1) + '_0_'] = False
    settings.values['_switch_' + str(spin-1) + '_1_'] = False
    settings.values['_switch_' + str(spin-1) + '_2_'] = False
    settings.values['_switch_' + str(spin-1) + '_3_'] = False
    settings.values['_switch_' + str(spin-1) + '_4_'] = False
    settings.values['_switch_' + str(spin-1) + '_5_'] = False
    settings.values['_switch_' + str(spin-1) + '_6_'] = False
    settings.values['_switch_' + str(spin-1) + '_7_'] = False
    # settings.values['_step_' + str(spin) + '_'] = '0'
    settings.values['_ana_00_' + str(spin-1) + '_'] = '0'
    settings.values['_ana_01_' + str(spin-1) + '_'] = '0'
    settings.values['_ana_02_' + str(spin-1) + '_'] = '0'
    settings.values['_ana_03_' + str(spin-1) + '_'] = '0'
    settings.values['_ana_04_' + str(spin-1) + '_'] = '0'
    settings.values['_ana_05_' + str(spin-1) + '_'] = '0'

    # now shift everything after location to +1 time point
    #print('Location: ', location)
    #print('Num points:', int((len(settings.values)-settings.other_items)/settings.items_per_row))

    end = int((len(settings.values)-settings.other_items)/settings.items_per_row) - 2
    start = location -1

    for l in range(end, start , -1 ): # travels backwards
        settings.values['_mode_'   + str(l+1) + '_']    = settings.values['_mode_'   + str(l) + '_']
        settings.values['_delay_'  + str(l+1) + '_']    = settings.values['_delay_'  + str(l) + '_']
        settings.values['_switch_' + str(l+1) + '_0_']  = settings.values['_switch_' + str(l) + '_0_']
        settings.values['_switch_' + str(l+1) + '_1_']  = settings.values['_switch_' + str(l) + '_1_']
        settings.values['_switch_' + str(l+1) + '_2_']  = settings.values['_switch_' + str(l) + '_2_']
        settings.values['_switch_' + str(l+1) + '_3_']  = settings.values['_switch_' + str(l) + '_3_']
        settings.values['_switch_' + str(l+1) + '_4_']  = settings.values['_switch_' + str(l) + '_4_']
        settings.values['_switch_' + str(l+1) + '_5_']  = settings.values['_switch_' + str(l) + '_5_']
        settings.values['_switch_' + str(l+1) + '_6_']  = settings.values['_switch_' + str(l) + '_6_']
        settings.values['_switch_' + str(l+1) + '_7_']  = settings.values['_switch_' + str(l) + '_7_']
        settings.values['_ana_00_'     + str(l+1) + '_']    = settings.values['_ana_00_'     + str(l) + '_']
        settings.values['_ana_01_'   + str(l+1) + '_']    = settings.values['_ana_01_'   + str(l) + '_']
        settings.values['_ana_02_' + str(l+1) + '_']    = settings.values['_ana_02_' + str(l) + '_']
        settings.values['_ana_03_'+ str(l+1) + '_']    = settings.values['_ana_03_'+ str(l) + '_']
        settings.values['_ana_04_'+ str(l+1) + '_']    = settings.values['_ana_04_'+ str(l) + '_']
        settings.values['_ana_05_'+ str(l+1) + '_']    = settings.values['_ana_05_'+ str(l) + '_']


    return settings.values



















def sequence_to_instructions_insert_or_delete(file_name = 'exp_sequence.csv'):
    # this turns the new sequence from insertion to instructions
    read_sequence(file_name)
    settings.instructions  = []
    spin = int(settings.sequence['_spin_'])
    iter = str(settings.sequence['_iter_'])
    num_rows = int((len(settings.sequence) - settings.other_items)/settings.items_per_row)

    for row in range(spin):
        row_switch = ['']*settings.digital_channels

        mode = settings.sequence[str('_mode_'+str(row)+'_')]
        delay = settings.sequence[str('_delay_'+str(row)+'_')]

        for col in range(settings.digital_channels):
            row_switch[col] = settings.sequence[str('_switch_' + str(row) + '_' + str(col) + '_' )]

        ana_00 = settings.sequence[str('_ana_00_'+str(row)+'_')]
        ana_01 = settings.sequence[str('_ana_01_'+str(row)+'_')]
        ana_02 = settings.sequence[str('_ana_02_'+str(row)+'_')]
        ana_03 = settings.sequence[str('_ana_03_'+str(row)+'_')]
        ana_04 = settings.sequence[str('_ana_04_'+str(row)+'_')]
        ana_05 = settings.sequence[str('_ana_05_'+str(row)+'_')]

        row_specs = [mode, delay, row_switch, ana_00, ana_01, ana_02, ana_03, ana_04, ana_05]
        settings.instructions.append(row_specs)

    return settings.instructions













def delete(location):
    # this function deletes a time point from the program
    # - updates the values (dictionary)
    # - updates the .csv file by changing the number of spinners
    # - copying the row right before it and add this row
    # - then shifting everything after by one time point.
    # - then restarting the window.
    # input: the location of insertion

    read_sequence()
    settings.values['_spin_'] = str(int(settings.values['_spin_']) - 1) # spinners increase by 1.
    spin = int(settings.values['_spin_'])
    iter = str(settings.values['_iter_'])
    num_rows = int((len(settings.values) - settings.other_items)/settings.items_per_row)

    # first shift everything after location to -1 time point
    # print('Location: ', location)
    # print('Num points:', int((len(settings.values)-settings.other_items)/settings.items_per_row))
    for l in range(location, int((len(settings.values)-settings.other_items)/settings.items_per_row)-1): # travels forward
        settings.values['_mode_'   + str(l) + '_']    = settings.values['_mode_'   + str(l+1) + '_']
        settings.values['_delay_'  + str(l) + '_']    = settings.values['_delay_'  + str(l+1) + '_']
        settings.values['_switch_' + str(l) + '_0_']  = settings.values['_switch_' + str(l+1) + '_0_']
        settings.values['_switch_' + str(l) + '_1_']  = settings.values['_switch_' + str(l+1) + '_1_']
        settings.values['_switch_' + str(l) + '_2_']  = settings.values['_switch_' + str(l+1) + '_2_']
        settings.values['_switch_' + str(l) + '_3_']  = settings.values['_switch_' + str(l+1) + '_3_']
        settings.values['_switch_' + str(l) + '_4_']  = settings.values['_switch_' + str(l+1) + '_4_']
        settings.values['_switch_' + str(l) + '_5_']  = settings.values['_switch_' + str(l+1) + '_5_']
        settings.values['_switch_' + str(l) + '_6_']  = settings.values['_switch_' + str(l+1) + '_6_']
        settings.values['_switch_' + str(l) + '_7_']  = settings.values['_switch_' + str(l+1) + '_7_']
        # settings.values['_step_'   + str(l) + '_']    = settings.values['_step_'   + str(l+1) + '_']
        settings.values['_ana_00_'     + str(l) + '_']    = settings.values['_ana_00_'     + str(l+1) + '_']
        settings.values['_ana_01_'   + str(l) + '_']    = settings.values['_ana_01_'   + str(l+1) + '_']
        settings.values['_ana_02_' + str(l) + '_']    = settings.values['_ana_02_' + str(l+1) + '_']
        settings.values['_ana_03_'+ str(l) + '_']    = settings.values['_ana_03_'+ str(l+1) + '_']
        settings.values['_ana_04_'+ str(l) + '_']    = settings.values['_ana_04_'+ str(l+1) + '_']
        settings.values['_ana_05_'+ str(l+1) + '_']    = settings.values['_ana_05_'+ str(l+1) + '_']

    # next removes the last row

    print('New spin is: ', spin)

    del settings.values['_mode_' + str(spin) + '_']
    del settings.values['_delay_' + str(spin) + '_']
    del settings.values['_switch_' + str(spin) + '_0_']
    del settings.values['_switch_' + str(spin) + '_1_']
    del settings.values['_switch_' + str(spin) + '_2_']
    del settings.values['_switch_' + str(spin) + '_3_']
    del settings.values['_switch_' + str(spin) + '_4_']
    del settings.values['_switch_' + str(spin) + '_5_']
    del settings.values['_switch_' + str(spin) + '_6_']
    del settings.values['_switch_' + str(spin) + '_7_']
    # del settings.values['_step_' + str(spin) + '_']
    del settings.values['_ana_00_' + str(spin) + '_']
    del settings.values['_ana_01_' + str(spin) + '_']
    del settings.values['_ana_02_' + str(spin) + '_']
    del settings.values['_ana_03_' + str(spin) + '_']
    del settings.values['_ana_04_' + str(spin) + '_']
    del settings.values['_ana_05_' + str(spin) + '_']

    return settings.values














def sequence_to_instructions_delete(file_name = 'exp_sequence.csv'):
    # this turns the new sequence from deletion to instructions
    read_sequence(file_name)
    settings.instructions  = []
    spin = int(settings.sequence['_spin_'])
    iter = str(settings.sequence['_iter_'])
    num_rows = int((len(settings.sequence) - settings.other_items)/settings.items_per_row)

    for row in range(spin):
        row_switch = ['']*settings.digital_channels

        mode = settings.sequence[str('_mode_'+str(row)+'_')]
        delay = settings.sequence[str('_delay_'+str(row)+'_')]

        for col in range(settings.digital_channels):
            row_switch[col] = settings.sequence[str('_switch_' + str(row) + '_' + str(col) + '_' )]

        # step = settings.sequence[str('_step_'+str(row)+'_')]
        ana_00 = settings.sequence[str('_ana_00_'+str(row)+'_')]
        ana_01 = settings.sequence[str('_ana_01_'+str(row)+'_')]
        ana_02 = settings.sequence[str('_ana_02_'+str(row)+'_')]
        ana_03 = settings.sequence[str('_ana_03_'+str(row)+'_')]
        ana_04 = settings.sequence[str('_ana_04_'+str(row)+'_')]
        ana_05 = settings.sequence[str('_ana_05_'+str(row)+'_')]

        row_specs = [mode, delay, row_switch, ana_00, ana_01, ana_02, ana_03, ana_04, ana_05]
        settings.instructions.append(row_specs)

    return settings.instructions










def scan_parameters():
    # first prints the scanning
    read_sequence()
    print('Scan mechanism: ', settings.sequence['_scan_mech_'])

    if settings.sequence['_scan_delay_'] == 'True' and settings.sequence['_scan_volt_'] == 'False': # don't recommend doing both...
        print('Delay start (s): ', settings.sequence['_scan_delay_start_'])
        print('Delay end (s): ', settings.sequence['_scan_delay_end_'])
        print('Step (s):', settings.sequence['_step_delay_'])

        # scan params for this option: analog delay scan
        settings.scan_parameters = {
                                    'Scan mechanism: ': settings.sequence['_scan_mech_'],
                                    'Time point: ': settings.sequence['_scan_ev_'],
                                    'Delay start (s): ': settings.sequence['_scan_delay_start_'],
                                    'Delay end (s): ': settings.sequence['_scan_delay_end_'],
                                    'Step (s):': settings.sequence['_step_delay_']
                                    }

    elif settings.sequence['_scan_volt_'] == 'True' and settings.sequence['_scan_delay_'] == 'False': # again, don't recommend doing both...
        print('Volts start (V): ', settings.sequence['_scan_volt_start_'])
        print('Volts end (V): ', settings.sequence['_scan_volt_end_'])
        print('Step (V):', settings.sequence['_step_volt_'])
        print('Voltage channel: ', settings.sequence['_volt_chan_'])

        # scan params for this option: analog voltage scan
        settings.scan_parameters = {
                                    'Scan mechanism: ': settings.sequence['_scan_mech_'],
                                    'Time point: ': settings.sequence['_scan_ev_'],
                                    'Volts start (V): ': settings.sequence['_scan_volt_start_'],
                                    'Volts end (V): ': settings.sequence['_scan_volt_end_'],
                                    'Step (V):': settings.sequence['_step_volt_'],
                                    'Voltage channel: ': settings.sequence['_volt_chan_']
                                    }

    elif settings.sequence['_scan_volt_'] == 'True' and settings.sequence['_scan_delay_'] == 'True': # don't recommend doing both
        sg.Popup('Popup', 'Scanning both delay and voltage not supported')

    elif settings.sequence['_scan_delay_'] == 'False' and settings.sequence['_scan_volt_'] == 'False': # if nothing is selected
        sg.Popup('Popup', 'Please select delay or voltage to scan!')

    else:
        print('hello kitty')

    return settings.scan_parameters





def make_instructions():
    num_events = int((len(settings.sequence)-settings.other_items)/settings.items_per_row)
    # creates analog wave
    for e in range(num_events):
        mode_e = str(settings.sequence['_mode_' + str(e) + '_'])
        if str(settings.sequence['_delay_' + str(e) + '_']) == '':
            duration_e = float(0.0)
        else:
            duration_e = float(settings.sequence['_delay_' + str(e) + '_'])
        if str(settings.sequence['_ana_00_' + str(e) + '_']) == '':
            ana_00_e = float(0.0)
        else:
            ana_00_e = float(settings.sequence['_ana_00_' + str(e) + '_'])
        if str(settings.sequence['_ana_01_' + str(e) + '_']) == '':
            ana_01_e = float(0.0)
        else:
            ana_01_e = float(settings.sequence['_ana_01_' + str(e) + '_'])
        if str(settings.sequence['_ana_02_' + str(e) + '_']) == '':
            ana_02_e = float(0.0)
        else:
            ana_02_e = float(settings.sequence['_ana_02_' + str(e) + '_'])
        if str(settings.sequence['_ana_03_' + str(e) + '_']) == '':
            ana_03_e = float(0.0)
        else:
            ana_03_e = float(settings.sequence['_ana_03_' + str(e) + '_'])
        if str(settings.sequence['_ana_04_' + str(e) + '_']) == '':
            ana_04_e = float(0.0)
        else:
            ana_04_e = float(settings.sequence['_ana_04_' + str(e) + '_'])
        if str(settings.sequence['_ana_05_' + str(e) + '_']) == '':
            ana_05_e = float(0.0)
        else:
            ana_05_e = float(settings.sequence['_ana_05_' + str(e) + '_'])
        # channel 1
        settings.ana_00.append([mode_e, duration_e, ana_00_e])
        # channel 2
        settings.ana_01.append([mode_e, duration_e, ana_01_e])
        # channel 3
        settings.ana_02.append([mode_e, duration_e, ana_02_e])
        # channel 4
        settings.ana_03.append([mode_e, duration_e, ana_03_e])
        # channel 5
        settings.ana_04.append([mode_e, duration_e, ana_04_e])
        # channel 6
        settings.ana_05.append([mode_e, duration_e, ana_05_e])

    # creates digital wave
    for event in range(num_events):
        state_number = 0
        for line in range(settings.digital_channels): # loop through each line
            switch_line = settings.sequence[str('_switch_' + str(event) + '_' + str(line) + '_' )]
            if switch_line == 'True':
                state_number = state_number + 2**line
            else:
                state_number = state_number
        # switch has the form [[state_number, delay]]
        settings.switch.append([state_number, float(settings.sequence['_delay_' + str(event) + '_'])])







def scan_voltage(scanning_channel = '', time_point = -1, volt_increment = 0):
    # does what it says: scans the voltage of a selected analog channel.
    # the digital channels and other analog channels are unaffected.

    num_events = int((len(settings.sequence)-settings.other_items)/settings.items_per_row)
    for e in range(num_events):
        # setting up everything as normal
        mode_e = str(settings.sequence['_mode_' + str(e) + '_'])
        if str(settings.sequence['_delay_' + str(e) + '_']) == '':
            duration_e = float(0.0)
        else:
            duration_e = float(settings.sequence['_delay_' + str(e) + '_'])
        if str(settings.sequence['_ana_00_' + str(e) + '_']) == '':
            ana_00_e = float(0.0)
        else:
            ana_00_e = float(settings.sequence['_ana_00_' + str(e) + '_'])
        if str(settings.sequence['_ana_01_' + str(e) + '_']) == '':
            ana_01_e = float(0.0)
        else:
            ana_01_e = float(settings.sequence['_ana_01_' + str(e) + '_'])
        if str(settings.sequence['_ana_02_' + str(e) + '_']) == '':
            ana_02_e = float(0.0)
        else:
            ana_02_e = float(settings.sequence['_ana_02_' + str(e) + '_'])
        if str(settings.sequence['_ana_03_' + str(e) + '_']) == '':
            ana_03_e = float(0.0)
        else:
            ana_03_e = float(settings.sequence['_ana_03_' + str(e) + '_'])
        if str(settings.sequence['_ana_04_' + str(e) + '_']) == '':
            ana_04_e = float(0.0)
        else:
            ana_04_e = float(settings.sequence['_ana_04_' + str(e) + '_'])
        if str(settings.sequence['_ana_05_' + str(e) + '_']) == '':
            ana_05_e = float(0.0)
        else:
            ana_05_e = float(settings.sequence['_ana_05_' + str(e) + '_'])

        # if at the correct time_point and channel, increment voltage
        if e+1 == time_point:
            if scanning_channel == '_ana_00_':
                ana_00_e += volt_increment
            if scanning_channel == '_ana_01_':
                ana_01_e += volt_increment
            if scanning_channel == '_ana_02_':
                ana_02_e += volt_increment
            if scanning_channel == '_ana_03_':
                ana_03_e += volt_increment
            if scanning_channel == '_ana_04_':
                ana_04_e += volt_increment
            if scanning_channel == '_ana_05_':
                ana_05_e += volt_increment

        settings.ana_00.append([mode_e, duration_e, ana_00_e])
        settings.ana_01.append([mode_e, duration_e, ana_01_e])
        settings.ana_02.append([mode_e, duration_e, ana_02_e])
        settings.ana_03.append([mode_e, duration_e, ana_03_e])
        settings.ana_04.append([mode_e, duration_e, ana_04_e])
        settings.ana_05.append([mode_e, duration_e, ana_05_e])

    # DIGITAL
    for event in range(num_events):
        state_number = 0
        for line in range(settings.digital_channels): # loop through each line
            switch_line = settings.sequence[str('_switch_' + str(event) + '_' + str(line) + '_' )]
            if switch_line == 'True':
                state_number = state_number + 2**line
            else:
                state_number = state_number
        # switch has the form [[state_number, delay]]
        settings.switch.append([state_number, float(settings.sequence['_delay_' + str(event) + '_'])])











def scan_delay(scan_step = 0.0, time_point = -1):
    # this function generates from the sequence the instructions for
    # the interpret(command) function to make the appropriate wave
    # this function is also used iteratively in single_array_scan_to_wave()


    make_instructions() # initialize the original wave
    num_events = int((len(settings.sequence)-settings.other_items)/settings.items_per_row)

    if scan_step != 0: # essentially if there is no DELAY scanning, then don't execute this part
        for e in range(num_events): # looping over all events
            if e == time_point: # but only add the scanning piece at the correct time point
                mode_e = str(settings.sequence['_mode_' + str(e) + '_'])
                # but one channel has some other value
                ana_00_e = float(settings.sequence['_ana_00_' + str(e-1) + '_'])
                settings.ana_00.insert(time_point - num_events, [mode_e, scan_step, ana_00_e])  # inserts value for scanning channel
                ana_01_e = float(settings.sequence['_ana_01_' + str(e-1) + '_'])
                settings.ana_01.insert(time_point - num_events, [mode_e, scan_step, ana_01_e])
                ana_02_e = float(settings.sequence['_ana_02_' + str(e-1) + '_'])
                settings.ana_02.insert(time_point - num_events, [mode_e, scan_step, ana_02_e])
                ana_03_e = float(settings.sequence['_ana_03_' + str(e-1) + '_'])
                settings.ana_03.insert(time_point - num_events, [mode_e, scan_step, ana_03_e])
                ana_04_e = float(settings.sequence['_ana_04_' + str(e-1) + '_'])
                settings.ana_04.insert(time_point - num_events, [mode_e, scan_step, ana_04_e])
                ana_05_e = float(settings.sequence['_ana_05_' + str(e-1) + '_'])
                settings.ana_05.insert(time_point - num_events, [mode_e, scan_step, ana_05_e])

                state_number = 0
                for line in range(settings.digital_channels): # loop through each line
                    switch_line = settings.sequence[str('_switch_' + str(e-1) + '_' + str(line) + '_' )]
                    if switch_line == 'True':
                        state_number = state_number + 2**line
                    else:
                        state_number = state_number
                # switch has the form [[state_number, delay]]

                settings.switch.insert(time_point - num_events, [state_number, scan_step])







def single_array_scan_to_wave(command = 'simulate'):
    # this function takes in the scan parameters and outputs a wave
    # this is called in the 'single-array' scan mode
    # basically this function just concatenates a bunch of waves from to_wave,
    # by default, this function simulates

    rate = float(settings.sequence['_rate_'])
    single_array = np.array([])
        # call to_wave() and concatenate or something...
        # DELAY SCAN
    if 'Delay start (s): ' in settings.scan_parameters: # if the scan mode is delay
        print('Scan mode is delay')
        number_of_steps = int( round((float(settings.scan_parameters['Delay end (s): ']) - float(settings.scan_parameters['Delay start (s): ']))/float(settings.scan_parameters['Step (s):'])))
        increment = float(settings.scan_parameters['Step (s):'])
        time_pt = int(settings.scan_parameters['Time point: '])

        for i in range(number_of_steps+1):
            scan_delay(scan_step = i*increment, time_point = time_pt) # call make instructions

        # this is to simulate
        if command == 'simulate':
            PCI.simulate(1, rate, PCI.to_wave(settings.ana_00, rate),
                                  PCI.to_wave(settings.ana_01, rate),
                                  PCI.to_wave(settings.ana_02, rate),
                                  PCI.to_wave(settings.ana_03, rate),
                                  PCI.to_wave(settings.ana_04, rate),
                                  PCI.to_wave(settings.ana_05, rate),
                                  PCI.to_digit(settings.switch, rate)
                                  )

        elif command == 'run':
            PCI.run(rate, PCI.to_wave(settings.ana_00, rate),
                                  PCI.to_wave(settings.ana_01, rate),
                                  PCI.to_wave(settings.ana_02, rate),
                                  PCI.to_wave(settings.ana_03, rate),
                                  PCI.to_wave(settings.ana_04, rate),
                                  PCI.to_wave(settings.ana_05, rate),
                                  PCI.to_digit(settings.switch, rate)
                                  )

        # reset waves to zeros
        settings.ana_00 = settings.ana_00*0
        settings.ana_01 = settings.ana_01*0
        settings.ana_02 = settings.ana_02*0
        settings.ana_03 = settings.ana_03*0
        settings.ana_04 = settings.ana_04*0
        settings.ana_05 = settings.ana_05*0
        settings.switch = []


    # VOLTAGE SCAN
    elif 'Volts start (V): ' in settings.scan_parameters: # if the analog scan mode is delay
        print('Scan mode is volt')
        number_of_steps = int( round((float(settings.scan_parameters['Volts end (V): ']) - float(settings.scan_parameters['Volts start (V): ']))/float(settings.scan_parameters['Step (V):'])))
        volt = float(settings.scan_parameters['Step (V):'])
        time_pt = int(settings.scan_parameters['Time point: '])
        chan_name = str(settings.scan_parameters['Voltage channel: '])

        for i in range(number_of_steps+1):
            scan_voltage(scanning_channel = chan_name, time_point = time_pt, volt_increment = i*volt) # call make instructions

        # this is to simulate
        if command == 'simulate':
            PCI.simulate(1, rate, PCI.to_wave(settings.ana_00, rate),
                                  PCI.to_wave(settings.ana_01, rate),
                                  PCI.to_wave(settings.ana_02, rate),
                                  PCI.to_wave(settings.ana_03, rate),
                                  PCI.to_wave(settings.ana_04, rate),
                                  PCI.to_wave(settings.ana_05, rate),
                                  PCI.to_digit(settings.switch, rate)
                                  )

        elif command == 'run':
            PCI.run(rate, PCI.to_wave(settings.ana_00, rate),
                                  PCI.to_wave(settings.ana_01, rate),
                                  PCI.to_wave(settings.ana_02, rate),
                                  PCI.to_wave(settings.ana_03, rate),
                                  PCI.to_wave(settings.ana_04, rate),
                                  PCI.to_wave(settings.ana_05, rate),
                                  PCI.to_digit(settings.switch, rate)
                                  )

        # reset waves to zeros
        settings.ana_00 = settings.ana_00*0
        settings.ana_01 = settings.ana_01*0
        settings.ana_02 = settings.ana_02*0
        settings.ana_03 = settings.ana_03*0
        settings.ana_04 = settings.ana_04*0
        settings.ana_05 = settings.ana_05*0
        settings.switch = []



    return








def multi_array_scan_to_wave():
        print('Functionality not yet implemented')










def interpret(command):
    # this function translates the instructions on Board
    # into data to be sent to PCI
    rate = float(settings.sequence['_rate_'])
    spin = int(settings.sequence['_spin_'])
    iter = str(settings.sequence['_iter_'])

    make_instructions()

    if command == 'simulate':
        PCI.simulate(1, rate, PCI.to_wave(settings.ana_00, rate),
                              PCI.to_wave(settings.ana_01, rate),
                              PCI.to_wave(settings.ana_02, rate),
                              PCI.to_wave(settings.ana_03, rate),
                              PCI.to_wave(settings.ana_04, rate),
                              PCI.to_wave(settings.ana_05, rate),
                              PCI.to_digit(settings.switch, rate)
                              )

    elif command == 'run':
        PCI.run(iter, rate, PCI.to_wave(settings.ana_00, rate),
                      PCI.to_wave(settings.ana_01, rate),
                      PCI.to_wave(settings.ana_02, rate),
                      PCI.to_wave(settings.ana_03, rate),
                      PCI.to_wave(settings.ana_04, rate),
                      PCI.to_wave(settings.ana_05, rate),
                      PCI.to_digit(settings.switch, rate)
                      )

    else:
        print('Invalid command')

    # reset waves to zeros
    settings.ana_00 = settings.ana_00*0
    settings.ana_01 = settings.ana_01*0
    settings.ana_02 = settings.ana_02*0
    settings.ana_03 = settings.ana_03*0
    settings.ana_04 = settings.ana_04*0
    settings.ana_05 = settings.ana_05*0
    settings.switch = []

    return








def make_view_window(initial_num_points = 10):
    # this function generates a window just to view procedure files
    # not intended to be edited.
    # this function is very much like make_window() except it has much fewer features
    # this function make the main window with a certain layout
    # layout is defined in GUI_functions
    # obtain experimental specs from exp_sequence.txt
    # the sequence is a global var defined in settings.py
    sg.ChangeLookAndFeel('Purple')
    settings.new_time_points_view = int(settings.sequence['_spin_'])
    settings.old_time_points_view = int((len(settings.sequence) - settings.other_items)/settings.items_per_row)

    settings.window_view = sg.Window('PREVIEW-PREVIEW-PREVIEW-PREVIEW-PREVIEW-PREVIEW',
                   default_element_size=(90, 1),
                   grab_anywhere=True).Layout(GUI.layout_main(initial_num_points))

    while True:
        settings.event_view, settings.values_view = settings.window_view.Read()
        if settings.event_view is None:
            break
        if settings.event_view == 'Exit' or settings.event_view == 'EXIT':
            settings.window_view.Close()
            return
        if settings.event_view == 'About':
            sg.Popup('Experimental Control', 'Created by Huan Q Bui\n Summer 2019')
        del settings.values_view[0]
    settings.window_view.Close()
    return












def make_window(initial_num_points):
    # this function make the main window with a certain layout
    # layout is defined in GUI_functions
    # obtain experimental specs from exp_sequence.txt
    # the sequence is a global var defined in settings.py
    sg.ChangeLookAndFeel('GreenTan')
    settings.new_time_points = int(settings.sequence['_spin_'])
    # print('New time points: ', settings.new_time_points)
    settings.old_time_points = int((len(settings.sequence) - settings.other_items)/settings.items_per_row)
    # print('Old time points: ', settings.old_time_points)

    settings.window = sg.Window('Experimental Control - PCI-6733',
                   default_element_size=(90, 1),
                   grab_anywhere=True).Layout(GUI.layout_main(initial_num_points))


    # GUI.generate_graph(window)

    settings.inserted = False
    settings.deleted = False
    settings.ramped = False


    while True:

        settings.ignore = True # this is the default status of ignore.
        # constantly updating for events/values
        settings.event, settings.values = settings.window.Read()
        if settings.event is None:
            break
        else:
            print(settings.event)
        # check for a new number of time points
        # settings.new_time_points = int(settings.values['_spin_'])

        if settings.event == 'Exit':
            quit()

        if settings.event == 'About':
            sg.Popup('Experimental Control', 'Created by Huan Q Bui\n Summer 2019')

        # check for change in number of rows
        if settings.event == '_spin_':
            update_sequence()
            sequence_to_instructions_spin()
            break

        for location in range(settings.new_time_points):
            # check for insertion
            if settings.event == '_insert_' + str(location) + '_':
                # print(settings.values)
                # print('Newer time points: ', settings.new_time_points)
                insert(location)
                sequence_to_instructions_insert_or_delete()
                settings.inserted = True
                update_sequence()
                settings.window.Close()
                return

                # check for deletion
            if settings.event == '_delete_' + str(location) + '_':
                update_sequence()
                delete(location)
                sequence_to_instructions_insert_or_delete()
                settings.deleted = True
                update_sequence()
                settings.window.Close()
                return

            # check for clicking the ramping option
            if settings.event == '_mode_' + str(location) + '_':
                settings.ramped = True
                update_sequence()
                # settings.window.Close()
                # return

        # save settings
        if settings.event == 'Apply' or settings.event == 'Apply settings':
            update_sequence_and_check_errors()
            # if settings.ignore is True:
            #     break # if ignore then just do it
            if settings.ignore is False: # I know this is redundant but it's easy to read
                settings.event = None # then nothing happens
                update_sequence()
                # settings.window.Close()
                # return
        # save settings + plot
        if settings.event == 'Plot data':
            # turns instructions into waveform to be sent
            # when data is sent, program simulates the waveform
            update_sequence_and_check_errors()
            if settings.ignore is True:
                interpret('simulate') # then just do it
                settings.event = None
            elif settings.ignore is False: # I know this is redundant but it's easy to read
                settings.event = None # then nothing happens
                update_sequence()
                settings.window.Close()
                return

        if settings.event == 'RUN':
            # when sequence is run, data is sent to PCI
            update_sequence()
            interpret('run')
            settings.event = None

        if settings.event == 'STOP':
            sg.Popup('?', 'No sequence is running!')

        if settings.event == 'EXIT':
            settings.window.Close()
            quit()

        if settings.event == 'Simulate':
            # if press scan then do something
            update_sequence()
            scan_parameters()
            if settings.scan_parameters['Scan mechanism: '] == 'Single-array Multi-sweep':
                single_array_scan_to_wave('simulate')
            elif settings.scan_parameters['Scan mechanism: '] == 'Multi-array Single-sweep':
                multi_array_scan_to_wave()

        if settings.event == 'SCAN':
            # if press scan then do something
            update_sequence()
            scan_parameters()
            if settings.scan_parameters['Scan mechanism: '] == 'Single-array Multi-sweep':
                single_array_scan_to_wave('run')
                print('Single-array Multi-sweep')
            elif settings.scan_parameters['Scan mechanism: '] == 'Multi-array Single-sweep':
                print('Multi-array Single-sweep')

            settings.event = None

        if settings.event == 'Preview':
            settings.file_name = settings.values['Browse']
            if settings.file_name == '':
                settings.file_name = 'exp_sequence.csv' # if nothing then set as default file
            settings.sequence = read_sequence(settings.file_name)
            sequence_to_instructions_spin(settings.file_name)
            make_view_window() # make window just to view
            sequence_to_instructions_spin('exp_sequence.csv') # once preview is done, then reset


        if settings.event == 'LOAD':
            settings.file_name = settings.values['Browse']
            if settings.file_name == '':
                settings.file_name = 'exp_sequence.csv' # if nothing then set as default file
            settings.sequence = read_sequence(settings.file_name)
            settings.window.Close()
            return

        if settings.event == 'SAVE': # save sequence as .csv
            settings.save_as = settings.values['Save As...']
            record_sequence(settings.values, settings.save_as)



        del settings.values[0]

    update_sequence()
    print('Window closing...')
    settings.window.Close()
    return
