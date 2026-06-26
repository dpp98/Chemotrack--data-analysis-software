#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 17:39:45 2025

@author: devi
"""

import math
import numpy as np
#import matplotlib.pyplot as plt

fileread = open('Full Results for Pos14.csv','r')
fileout = open('Results_theta_0_100uM_14_05_2026.csv','a')

cmax_exp = 100000.0
cmin_exp = 0.0

len_tracks = []

######## Shouldn't have to change anything below this line ###############

xmin = 0.0
xmax = 1000.0
dcdx = (cmax_exp-cmin_exp)/(xmax-xmin)

s = fileread.readline()
myid = -100
track_x = []
track_y = []
c = []
cei = []
xc = []
segl = 5
segtime = (segl-1)*0.5 # in minutes
numtracks = 0

dist_cap = 15.0 # Minimum distance moved by a cell in one segment

for s in fileread:
    
    split = s.split(',')
    
    tid = int(split[1])
    x1 = float(split[3])
    y1 = float(split[4])
    
    if (x1 > xmax):
        print('error')
    
    if tid == myid:   # old track continuing
        
        track_x = np.append(track_x,x1)
        track_y = np.append(track_y,y1)        

    else:           # New track
        
        numtracks += 1
        #print('New Track found', myid, tid)
        #print('Analyzing the old track')
        
        trackl = int(len(track_x))
        numseg = int(trackl/segl)
        
        for j in range(numseg):
            
            start = j*(segl - 1)
            end = start + segl - 1
            
            delx = track_x[end] - track_x[start]
            dely = track_y[end] - track_y[start]
      
            totdist = 0
            
            for k in range(segl - 1):
                totdist += math.sqrt((track_x[start+k+1]-track_x[start+k])**2 + (track_y[start+k+1]-track_y[start+k])**2)
                
            if delx > totdist:
                print(totdist, delx, j)
                print(track_x)
                print(track_y)
                print("------------------------------------------------------")
            
            if totdist > dist_cap:
                myx = 0.5*(track_x[start] + track_x[end])
                angle = np.arctan2(dely,delx)
                speed = totdist / segtime
                local_conc = myx*dcdx+cmin_exp
                chemotactic_index = delx/totdist
                
                c = np.append(c,local_conc)
                cei = np.append(cei,chemotactic_index)
                xc = np.append(xc,myx)
                fileout.write(str(myx)+" "+str(local_conc)+" "+str(chemotactic_index)+" "+str(angle)+" "+str(speed))
                fileout.write("\n")
        
        track_x = []
        track_y = []
        
        # start recording new track
        
        track_x = np.append(track_x,x1)
        track_y = np.append(track_y,y1)

        myid = tid
        


#plt.scatter(xc,cei,s=0.1)
#plt.show()

fileread.close()
fileout.close()
