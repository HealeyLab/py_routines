# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 09:37:50 2021

@author: Luke
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 14:31:30 2019

@author: Healey (Luke Remage-Healey)
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.size'] = 18.0
import pandas as pd
import csv

from pylab import *


"""this is a routine to take kilosort sorted spikes (timestamps in '.txt' files)
and trigger them with a stimulus key (typically a '.csv' format) to generate a raster, PSTH, 
and inst FR plot for a given stimulus. beware, this code is quite nested and slow...."""

def run_folder(ky, winstart, winend):
    """runs an entire folder's collection of sorted 'txt' files"""
    
    l = os.listdir()
    for i in l:
        if i.endswith('.txt'):
            print(i)
            raster_H_FR(ky, readspikes(i), str('' + i[-7:-4] + ''), 0, 3000, winstart, winend)
    return


def key(csvfile, start, end):
    """returns the timestamps of the kilosort  stimulations in 'csvfile' as a dict
    with the restriction of the 'start' and 'end' times of the recording"""
#    """and all values are multiplied 1000x"""
    t=[]
    #    d=[]
    
    with open(csvfile,'r') as myfile:
        myreader=csv.reader(myfile, delimiter=',', quotechar='"')
        for row in myreader:
            t.append(float(row[0]))
    #            d.append(float(row[1]))
    
    temp = [] 
    for i in range(len(t)):
        if t[i] < start:
            continue
        if t[i] > end:
            continue
        else:
            temp.append(t[i]) #, d[i]])
     
    return temp



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

  
def raster_H_FR(keys, clus, clusname, start, end, ras_start, ras_end):
    '''Takes a set of key triggers 'keys', a sorted spike cluster 'clus', the name of the cluster
    for plotting on the figure 'clusname' as a string, the 'start' and
    'end' of a segment of recording, and the frames for the raster start 'ras_start' and 
    raster end 'ras_end', to generate a peristimulus raster histogram, and FR plot on the same plot'''
   
    # below generates the rasterized spikes
    a = {}
    for i in keys:
        temp = []
        for j in clus:
            if j > start:
                if j < end:
                    if j > i-ras_start:
                        if j < i + ras_end:
                            temp.append(j-i)
        a[i] = temp
    s = pd.Series(a)   #this above generates the raster as a pandas data series
    
    #below generates the histogram bins
    bins=[]
    for i in np.arange(-ras_start, ras_end+0.005, 0.005):   #to use arange, which allows decimals
        bins.append(round(i,3))     #to round the float to 2 decimal places  

    

    #below plots all three on the same axes
    f = plt.figure('' + str(clusname) + '')
    plt.subplot(3,1,1)       #pos is a three digit integer, where the first digit is the number of rows, the second the number of columns, and the third the index of the subplot.
    plt.eventplot(s)    #to plot the raster
    plt.box(False)
    #    plt.xaxis(False)
    
    plt.subplot(3,1,2)
    b = plt.hist(s, bins, stacked=True, width=0.01, label = 'hist') #to plot the PSTH
    #plt.ylim(0, int(max(hist.values()))+5)
    
    plt.ylabel('spikes per bin')
    
    #plt.legend()
    
    #below generates the instantaneous FR plot   
    FR = pd.DataFrame(b[0]).transpose()       #grab the first tuple of rasterized spikes from hist
                
    bins2 = bins.copy()
    bins2.pop(-1)     #take last one off since hist lops it off
    
    FR['ave'], FR['std'] = np.mean(FR, axis=1), np.std(FR, axis=1)
    FR['sterr'] = np.std(FR, axis=1)/np.sqrt(len(FR.columns))
    FR['x'] = bins2
    
    plt.subplot(3,1,3) #to plot the instantaneous FR
    plt.plot(FR['x'], FR['ave'])
    plt.fill_between(FR['x'], (FR['ave']+FR['sterr']), (FR['ave']-FR['sterr']), facecolor='blue', alpha=0.5)
    plt.ylabel('FR')
    plt.xlabel('Time (sec)')
    
    plt.show()


    return FR         


