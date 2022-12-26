# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 12:49:53 2021

@author: Luke RH
Based on arduino base code by Dan Pollak, dpollak@caltech.edu

protocol to deliver randomized playback of audio stimuli via RPi. 

"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
from datetime import datetime

from scipy.io.wavfile import write

from pymata4 import pymata4

import simpleaudio as sa


#User input definitions
reps = 5           #Define number of playback repetitions

isi = 6            #Define inter-stimulus interval


# pymata4 uses expressfirmata
board = pymata4.Pymata4(com_port="COM4")
# https://mryslab.github.io/pymata4/device_writes/

# # Audio STA
board.set_pin_mode_digital_output(6)


folder_list = os.listdir()        #list out the .wav files in the CWD

stim_list = []
for file in folder_list:
    if file.endswith(".wav"):
        stim_list.append(file)          #only include filenames that are .wav

stim_list = stim_list*reps              #get all stimulus repetitions in the list


np.random.shuffle(stim_list)            #rando


for file in stim_list:
    # Skip if it's file junk
    if not file.endswith(".wav"):
        continue
    filename = os.path.join(file)
    
    # Load wav
    wave_obj = sa.WaveObject.from_wave_file(filename)
    
    # Play 
    play_obj = wave_obj.play()
    
    # Notify DAQ it's playing
    board.digital_write(6, 1)
    
    # Wait until sound has finished playing
    play_obj.wait_done()  
    
    # Notify DAQ it has stopped
    board.digital_write(6, 0)
    
    # Sleep
    time.sleep(isi)
    
pd.DataFrame({"wav":stim_list}).to_csv(datetime.now().strftime("%d-%m-%Y_%H-%M-%S.csv"))

