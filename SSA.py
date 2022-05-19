# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 09:24:21 2022

@author: Luke Remage-Healey

"""

"""Adaptation rates were calculated using trials 6–25, which is the approximate-
linear phase of the adaptation profile in NCM (Phan et al.,
2006). For each stimulus, the stimulus firing rate across trials was normalized
by the firing on trial 6 (set to 100%). Then, a linear regression
was calculated between trials 6 and 25. For each treatment, the minimum
(steepest) adaptation slope across stimuli was used for each unit.

from Macedo-Lima, Boyd, and Remage-Healey, 2021 J. Neurosci
"""


import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.size'] = 18.0
import pandas as pd
import csv

from pylab import *



def run_folder(ky, keyname, winstart, winend):
    """runs an entire folder's collection of sorted 'txt' files
    uses a key to raster spikes from the timestamps according to window open (winstart)
    and window end (winend). 'keyname' just passes an identifier to the plot"""
    
    slopes = {}
    l = os.listdir()
    for i in l:
        if i.endswith('.txt'):
            print(i)
            m = raster_for_SSA(ky, keyname, readspikes(i), str('' + i[-7:-4] + ''), 0, 3000, winstart, winend)
            slopes[str('' + i[-7:-4] + '_' + str(keyname) + ' ')] = m
    return slopes


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
    #plt.box(False)
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
    
    FRave, FRstd = np.mean(FR, axis=1), np.std(FR, axis=1)
    FRsterr = np.std(FR, axis=1)/np.sqrt(len(FR.columns))
    FRx = bins2
    
    plt.subplot(3,1,3) #to plot the instantaneous FR
    plt.plot(FRx, FRave)
    plt.fill_between(FRx, (FRave +FRsterr), (FRave -FRsterr), facecolor='blue', alpha=0.5)
    plt.ylabel('Inst. FR')
    plt.xlabel('Time (sec)')
    
    plt.figure()
    SSA_plot(s, clusname)
    plt.show()
    
    return s     

  
def raster_for_SSA(keys, keyname, clus, clusname, start, end, ras_start, ras_end):
    '''Takes a set of key triggers 'keys', 'keyname' just passes an identifier string to the plot,
    a sorted spike cluster 'clus', the name of the cluster
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
    
    
    plt.figure()
    sl = SSA_plot(s, keyname, clusname)
    plt.show()
    
    return sl     #return plot of SSA, and slope sl

def SSA_plot(s, keyname, clusname):
    """Takes in a rasterized pandas series 's' , 'keyname' just passes an identifier to the plot,
    and calculates avg firing rate adaptation 
    over all trials, plotting this and the slope"""
    
    b = eventplot(s)     #get data out of the eventplot raster
    plt.close()
    
    frone = []              #firing rate list for the first second after stimulus onset
    frtwo = []              #firing rate list for the second second after stimulus onset
    for i in range(len(b)):
        stamps = b[i].get_positions()           #retrieve the list of timestamps from the eventplot
        one = [j for j in stamps if 0<j<1]
        two = [k for k in stamps if 1<k<2]
        frone.append(len(one))
        frtwo.append(len(two))
    
    ssa = pd.DataFrame()
    
    ssa['one'] = frone
    ssa['two'] = frtwo
    
    ssa['ave'] = np.mean(ssa, axis = 1)
    
    plt.figure('' + str(str(clusname)) + ' SSA' + ' for stimulus = ' + str(keyname) + '')
    plt.plot(ssa['ave'])
    coef = np.polyfit(ssa.index, ssa['ave'], 1)
    poly1d_fn = np.poly1d(coef)
    slop = round(coef[0], ndigits=5)
    plt.plot(ssa.index, poly1d_fn(ssa.index), '--k')
    plt.ylim(0,75)
    plt.ylabel('Avg 1-sec FR (Hz)')
    plt.xlabel('Trial')
    plt.title('slope = ' + str(slop) +  ' ')
    
    #plt.show()
    
    return coef[0]


