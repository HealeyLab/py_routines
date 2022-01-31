# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 09:00:30 2021

@author: HealeyLab
"""


import os
#import neo
#import elephant
import pandas as pd
import numpy as np
import matplotlib as matplotlib  # for plotting
import matplotlib.pyplot as plt
#from neo import io

#from neo.core import Segment, SpikeTrain, AnalogSignal, Event
#from quantities import Hz, s
#import quantities as pq
import scipy
from scipy import signal



def LoadChan(arry):
    """takes an array from a continuous file in Rhythm_FPGA directory, sets it up
    as a dict of channels"""
    """to setup the flat binary as a dictionary of 32 channels"""
    channels = {}
    for j in range(32):
        channels['ch' + str(j)] = []
        for i in range(j, len(arry), 32):
            channels['ch' + str(j)].append(arry[i])
    
    return channels

#chan = np.load('channels.npy', allow_pickle=True)

def readspikes(spikes):
    
    """reads in a '.txt' kilosorted spike train into format for plotting"""
    myfile=open(spikes,'r')
    gadtxt=myfile.read()
    myfile.close()


    #convert txt into a list (do anything on the r in that one argument)
    gadsplit = gadtxt.split("\n")

    gadsplit = gadsplit[0:-1]

    #to make numbers work:    
    spks = [float(i) for i in gadsplit]
    
    return spks



def wave_plot(timestamps, clusname, filtered_voltage_channel, wave_N, width):
    
    """A function to plot waveforms from Kilosorted clusters from the original Intan binary
    channel, and return the averaged peak-to-peak duration. Takes in a set of Kilosorted single-unit 'timestamps' 
    from readspikes, a band-pass filtered Intan channel 'filtered_voltage_channel', 
    a user-defined sample of N waveforms 'wave_N',
    and a window 'width' for plotting the waveform average (typically 0.01 sec). """
    
    x=[]
    for i in range(len(filtered_voltage_channel)):
        x.append(i)
   
    xs = []
    for i in x:
        xs.append(x[i]/30000)   #set up time in seconds
    
    waves = {}    #set up the dictionary/DataFrame
    
    temp = []
    for j in timestamps[:wave_N]:   
        for i in range(len(xs)):
            if xs[i] > j - width:
                if xs[i] < j + width:
                    temp.append(filtered_voltage_channel[i])
        waves[j] = temp
        temp = []  
    
    wave = pd.DataFrame.from_dict(waves, orient='index')
    wave = wave.transpose()
    #wave.plot()
    
    avg = wave.mean(axis=1)
    sterr = wave.sem(axis=1)
    #avg.plot()
    
        
    plotx = xs[:wave.shape[0]]
    
    peak1 = plotx[avg.index[avg == np.max(avg)].tolist()[0]]
    
    peak2 = plotx[avg.index[avg == np.min(avg)].tolist()[0]]
    
    p2p = peak2-peak1
    
    plt.plot(plotx, avg)
    plt.fill_between(plotx, (avg+sterr), (avg-sterr), facecolor='gray', alpha=0.5)
    plt.vlines([peak1, peak2], np.max(avg), np.max(avg)+10, colors='red')
    plt.title('average of ' + str(wave_N) + ' ' + str(clusname) + ' APs with P2P duration ' + str(p2p)+ '')
    
    #plt.ylabel('FR')
    plt.show()

    return wave, plotx, avg, sterr


#Uses:

#arr = np.fromfile('continuous.dat', dtype='<i2', sep="")


#"""cluster118 is on ch17 tetrode 5"""


#channels = {}               #set up all 32 channels in a dict
#for j in range(32):
#    channels['ch' + str(j)] = []
#    for i in range(j, len(arr), 32):
#        channels['ch' + str(j)].append(arr[i])   #unpack the channels from the binary array 'arr'
        
#ch19 = channels['ch19']                           #grab channel for cluster 113

#del channels                                      #recover some RAM
#del arr                                            #recover more RAM


#spks113 = readspikes('11232021_experiment1_recording1_cluster113.txt')
#spks118 = readspikes('11232021_experiment1_recording1_cluster118.txt')

#chan16p = scipy.signal.butter(3, 600, btype='highpass', fs=30000, output='sos')         #set up bandpass filter to get rid of low-freq oscillations
#filteredch19 = signal.sosfilt(chan16p, ch19)                                #apply filter to channel

#wave19 = wave_plot(cl123, 'spikes123ch19', filteredch19, 450, 0.01)




