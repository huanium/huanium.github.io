import PySimpleGUI as sg
from tkinter import *
import GUI_functions as GUI_functions
import GUI_main
import settings
import nidaqmx
import math
import numpy as np
from nidaqmx import *
import matplotlib.pyplot as plt

# the settings library defines some global variables
if __name__ == "__main__":
    # runs the GUI on Loop
    # every change in the window results in a new refresh
    # The default number of time points is 5

    settings.init()
    GUI_main.sequence_to_instructions_spin()
    # GUI_main.sequence_to_instructions_insert()
    GUI_main.make_window(settings.default_num_pts)
    # GUI_main.update_sequence(settings.file_name)
    # GUI_main.sequence_to_instructions_insert()

    while True:

        if settings.event == '_spin_' or settings.new_time_points != settings.old_time_points:
            # print('New time points: ', settings.new_time_points)
            # print('Old time points: ', settings.old_time_points)
            GUI_main.sequence_to_instructions_spin()
            GUI_main.make_window(settings.new_time_points)

        # if inserted or deleted
        if settings.inserted == True or settings.deleted == True:
            # print('New time points: ', settings.new_time_points)
            # print('Old time points: ', settings.old_time_points)
            GUI_main.sequence_to_instructions_insert_or_delete()
            GUI_main.make_window(settings.new_time_points)

        if settings.event == 'Load sequence': # if specific instructions are being loaded
            print('File being loaded is: ', settings.file_name)
            # settings.sequence = GUI_main.read_sequence(settings.file_name)
            # print(settings.sequence)
            GUI_main.sequence_to_instructions_spin(settings.file_name)
            # settings.values = settings.sequence.copy()
            GUI_main.make_window(settings.default_num_pts)

# settings.new_time_points != settings.old_time_points or s
