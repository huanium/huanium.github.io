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
            ah = settings.sequence[str('_AH_'+str(row)+'_')]
            trap = settings.sequence[str('_Trap_'+str(row)+'_')]
            repump = settings.sequence[str('_Repump_'+str(row)+'_')]
            aom = settings.sequence[str('_aom_760_'+str(row)+'_')]
            vco = settings.sequence[str('_vco_760_'+str(row)+'_')]
            vca = settings.sequence[str('_vca_'+str(row)+'_')]

            row_specs = [mode, delay, row_switch, ah, trap, repump, aom, vco, vca]
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
            ah = settings.sequence[str('_AH_'+str(row)+'_')]
            trap = settings.sequence[str('_Trap_'+str(row)+'_')]
            repump = settings.sequence[str('_Repump_'+str(row)+'_')]
            aom = settings.sequence[str('_aom_760_'+str(row)+'_')]
            vco = settings.sequence[str('_vco_760_'+str(row)+'_')]
            vca = settings.sequence[str('_vca_'+str(row)+'_')]

            row_specs = [mode, delay, row_switch, ah, trap, repump, aom, vco, vca]
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
    settings.values['_AH_' + str(spin-1) + '_'] = '0'
    settings.values['_Trap_' + str(spin-1) + '_'] = '0'
    settings.values['_Repump_' + str(spin-1) + '_'] = '0'
    settings.values['_aom_760_' + str(spin-1) + '_'] = '0'
    settings.values['_vco_760_' + str(spin-1) + '_'] = '0'
    settings.values['_vca_' + str(spin-1) + '_'] = '0'

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
        settings.values['_AH_'     + str(l+1) + '_']    = settings.values['_AH_'     + str(l) + '_']
        settings.values['_Trap_'   + str(l+1) + '_']    = settings.values['_Trap_'   + str(l) + '_']
        settings.values['_Repump_' + str(l+1) + '_']    = settings.values['_Repump_' + str(l) + '_']
        settings.values['_aom_760_'+ str(l+1) + '_']    = settings.values['_aom_760_'+ str(l) + '_']
        settings.values['_vco_760_'+ str(l+1) + '_']    = settings.values['_vco_760_'+ str(l) + '_']
        settings.values['_vca_'+ str(l+1) + '_']    = settings.values['_vca_'+ str(l) + '_']


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

        # step = settings.sequence[str('_step_'+str(row)+'_')]
        ah = settings.sequence[str('_AH_'+str(row)+'_')]
        trap = settings.sequence[str('_Trap_'+str(row)+'_')]
        repump = settings.sequence[str('_Repump_'+str(row)+'_')]
        aom = settings.sequence[str('_aom_760_'+str(row)+'_')]
        vco = settings.sequence[str('_vco_760_'+str(row)+'_')]
        vca = settings.sequence[str('_vca_'+str(row)+'_')]

        row_specs = [mode, delay, row_switch, ah, trap, repump, aom, vco, vca]
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
        settings.values['_AH_'     + str(l) + '_']    = settings.values['_AH_'     + str(l+1) + '_']
        settings.values['_Trap_'   + str(l) + '_']    = settings.values['_Trap_'   + str(l+1) + '_']
        settings.values['_Repump_' + str(l) + '_']    = settings.values['_Repump_' + str(l+1) + '_']
        settings.values['_aom_760_'+ str(l) + '_']    = settings.values['_aom_760_'+ str(l+1) + '_']
        settings.values['_vco_760_'+ str(l) + '_']    = settings.values['_vco_760_'+ str(l+1) + '_']
        settings.values['_vca_'+ str(l+1) + '_']    = settings.values['_vca_'+ str(l+1) + '_']

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
    del settings.values['_AH_' + str(spin) + '_']
    del settings.values['_Trap_' + str(spin) + '_']
    del settings.values['_Repump_' + str(spin) + '_']
    del settings.values['_aom_760_' + str(spin) + '_']
    del settings.values['_vco_760_' + str(spin) + '_']
    del settings.values['_vca_' + str(spin) + '_']

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
        ah = settings.sequence[str('_AH_'+str(row)+'_')]
        trap = settings.sequence[str('_Trap_'+str(row)+'_')]
        repump = settings.sequence[str('_Repump_'+str(row)+'_')]
        aom = settings.sequence[str('_aom_760_'+str(row)+'_')]
        vco = settings.sequence[str('_vco_760_'+str(row)+'_')]
        vca = settings.sequence[str('_vca_'+str(row)+'_')]

        row_specs = [mode, delay, row_switch, ah, trap, repump, aom, vco, vca]
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
        if str(settings.sequence['_AH_' + str(e) + '_']) == '':
            AH_e = float(0.0)
        else:
            AH_e = float(settings.sequence['_AH_' + str(e) + '_'])
        if str(settings.sequence['_Trap_' + str(e) + '_']) == '':
            Trap_e = float(0.0)
        else:
            Trap_e = float(settings.sequence['_Trap_' + str(e) + '_'])
        if str(settings.sequence['_Repump_' + str(e) + '_']) == '':
            Repump_e = float(0.0)
        else:
            Repump_e = float(settings.sequence['_Repump_' + str(e) + '_'])
        if str(settings.sequence['_aom_760_' + str(e) + '_']) == '':
            aom_760_e = float(0.0)
        else:
            aom_760_e = float(settings.sequence['_aom_760_' + str(e) + '_'])
        if str(settings.sequence['_vco_760_' + str(e) + '_']) == '':
            vco_760_e = float(0.0)
        else:
            vco_760_e = float(settings.sequence['_vco_760_' + str(e) + '_'])
        if str(settings.sequence['_vca_' + str(e) + '_']) == '':
            vca_e = float(0.0)
        else:
            vca_e = float(settings.sequence['_vca_' + str(e) + '_'])
        # channel 1
        settings.AH.append([mode_e, duration_e, AH_e])
        # channel 2
        settings.Trap.append([mode_e, duration_e, Trap_e])
        # channel 3
        settings.Repump.append([mode_e, duration_e, Repump_e])
        # channel 4
        settings.aom.append([mode_e, duration_e, aom_760_e])
        # channel 5
        settings.vco.append([mode_e, duration_e, vco_760_e])
        # channel 6
        settings.vca.append([mode_e, duration_e, vca_e])

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
        if str(settings.sequence['_AH_' + str(e) + '_']) == '':
            AH_e = float(0.0)
        else:
            AH_e = float(settings.sequence['_AH_' + str(e) + '_'])
        if str(settings.sequence['_Trap_' + str(e) + '_']) == '':
            Trap_e = float(0.0)
        else:
            Trap_e = float(settings.sequence['_Trap_' + str(e) + '_'])
        if str(settings.sequence['_Repump_' + str(e) + '_']) == '':
            Repump_e = float(0.0)
        else:
            Repump_e = float(settings.sequence['_Repump_' + str(e) + '_'])
        if str(settings.sequence['_aom_760_' + str(e) + '_']) == '':
            aom_760_e = float(0.0)
        else:
            aom_760_e = float(settings.sequence['_aom_760_' + str(e) + '_'])
        if str(settings.sequence['_vco_760_' + str(e) + '_']) == '':
            vco_760_e = float(0.0)
        else:
            vco_760_e = float(settings.sequence['_vco_760_' + str(e) + '_'])
        if str(settings.sequence['_vca_' + str(e) + '_']) == '':
            vca_e = float(0.0)
        else:
            vca_e = float(settings.sequence['_vca_' + str(e) + '_'])

        # if at the correct time_point and channel, increment voltage
        if e+1 == time_point:
            if scanning_channel == '_AH_':
                AH_e += volt_increment
            if scanning_channel == '_Trap_':
                Trap_e += volt_increment
            if scanning_channel == '_Repump_':
                Repump_e += volt_increment
            if scanning_channel == '_aom_760_':
                aom_760_e += volt_increment
            if scanning_channel == '_vco_760_':
                vco_760_e += volt_increment
            if scanning_channel == '_vca_':
                vca_e += volt_increment

        settings.AH.append([mode_e, duration_e, AH_e])
        settings.Trap.append([mode_e, duration_e, Trap_e])
        settings.Repump.append([mode_e, duration_e, Repump_e])
        settings.aom.append([mode_e, duration_e, aom_760_e])
        settings.vco.append([mode_e, duration_e, vco_760_e])
        settings.vca.append([mode_e, duration_e, vca_e])

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
                AH_e = float(settings.sequence['_AH_' + str(e-1) + '_'])
                settings.AH.insert(time_point - num_events, [mode_e, scan_step, AH_e])  # inserts value for scanning channel
                Trap_e = float(settings.sequence['_Trap_' + str(e-1) + '_'])
                settings.Trap.insert(time_point - num_events, [mode_e, scan_step, Trap_e])
                Repump_e = float(settings.sequence['_Repump_' + str(e-1) + '_'])
                settings.Repump.insert(time_point - num_events, [mode_e, scan_step, Repump_e])
                aom_760_e = float(settings.sequence['_aom_760_' + str(e-1) + '_'])
                settings.aom.insert(time_point - num_events, [mode_e, scan_step, aom_760_e])
                vco_760_e = float(settings.sequence['_vco_760_' + str(e-1) + '_'])
                settings.vco.insert(time_point - num_events, [mode_e, scan_step, vco_760_e])
                vca_e = float(settings.sequence['_vca_' + str(e-1) + '_'])
                settings.vca.insert(time_point - num_events, [mode_e, scan_step, vca_e])

                state_number = 0
                for line in range(settings.digital_channels): # loop through each line
                    switch_line = settings.sequence[str('_switch_' + str(e-1) + '_' + str(line) + '_' )]
                    if switch_line == 'True':
                        state_number = state_number + 2**line
                    else:
                        state_number = state_number
                # switch has the form [[state_number, delay]]

                settings.switch.insert(time_point - num_events, [state_number, scan_step])







def single_array_scan_to_wave():
    # this function takes in the scan parameters and outputs a wave
    # this is called in the 'single-array' scan mode
    # basically this function just concatenates a bunch of waves from to_wave,

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
        PCI.simulate(1, rate, PCI.to_wave(settings.AH, rate),
                              PCI.to_wave(settings.Trap, rate),
                              PCI.to_wave(settings.Repump, rate),
                              PCI.to_wave(settings.aom, rate),
                              PCI.to_wave(settings.vco, rate),
                              PCI.to_wave(settings.vca, rate),
                              PCI.to_digit(settings.switch, rate)
                              )

        # reset waves to zeros
        settings.AH = settings.AH*0
        settings.Trap = settings.Trap*0
        settings.Repump = settings.Repump*0
        settings.aom = settings.aom*0
        settings.vco = settings.vco*0
        settings.vca = settings.vca*0
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
        PCI.simulate(1, rate, PCI.to_wave(settings.AH, rate),
                            PCI.to_wave(settings.Trap, rate),
                            PCI.to_wave(settings.Repump, rate),
                            PCI.to_wave(settings.aom, rate),
                            PCI.to_wave(settings.vco, rate),
                            PCI.to_wave(settings.vca, rate),
                            PCI.to_digit(settings.switch, rate)
                            )

        # reset waves to zeros
        settings.AH = settings.AH*0
        settings.Trap = settings.Trap*0
        settings.Repump = settings.Repump*0
        settings.aom = settings.aom*0
        settings.vco = settings.vco*0
        settings.vca = settings.vca*0
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
        PCI.simulate(1, rate, PCI.to_wave(settings.AH, rate),
                              PCI.to_wave(settings.Trap, rate),
                              PCI.to_wave(settings.Repump, rate),
                              PCI.to_wave(settings.aom, rate),
                              PCI.to_wave(settings.vco, rate),
                              PCI.to_wave(settings.vca, rate),
                              PCI.to_digit(settings.switch, rate)
                              )

    elif command == 'run':
        PCI.run(iter, rate, PCI.to_wave(settings.AH, rate),
                      PCI.to_wave(settings.Trap, rate),
                      PCI.to_wave(settings.Repump, rate),
                      PCI.to_wave(settings.aom, rate),
                      PCI.to_wave(settings.vco, rate),
                      PCI.to_wave(settings.vca, rate),
                      PCI.to_digit(settings.switch, rate)
                      )

    else:
        print('Invalid command')

    # reset waves to zeros
    settings.AH = settings.AH*0
    settings.Trap = settings.Trap*0
    settings.Repump = settings.Repump*0
    settings.aom = settings.aom*0
    settings.vco = settings.vco*0
    settings.vca = settings.vca*0
    settings.switch = []

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
                   grab_anywhere=False).Layout(GUI.layout_main(initial_num_points))


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
                single_array_scan_to_wave()
            elif settings.scan_parameters['Scan mechanism: '] == 'Multi-array Single-sweep':
                multi_array_scan_to_wave()

        if settings.event == 'SCAN':
            # if press scan then do something
            update_sequence()
            scan_parameters()
            if settings.scan_parameters['Scan mechanism: '] == 'Single-array Multi-sweep':
                print('Single-array Multi-sweep')
            elif settings.scan_parameters['Scan mechanism: '] == 'Multi-array Single-sweep':
                print('Multi-array Single-sweep')

            settings.event = None

        if settings.event == 'Load sequence':
            settings.file_name = settings.values['Browse']
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
