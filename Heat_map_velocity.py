# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:03:59 2019

@author: pm11lms
"""

from edempy import Deck
import math
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#-----------------#
#    Load data    # 
#-----------------#
d1 = Deck("0.4g/0.4g.dem")

#-----------------#
#  get timesteps  #
#-----------------#
t1 = d1.numTimesteps - 301


#----------------#
#  Heat map code #
#----------------#

def Heatmap(deck, t1, t2):
    Velocities = []
    Positions = []
    count = 0
    
    for j in range(t1, t2):
        try:
            vel = deck.timestep[j].particle[0].getVelocities()
            pos = deck.timestep[j].particle[0].getPositions()
            if count < 1:
                print("deck loaded")
                count+=1
            for i in range(0,len(vel)):
                Positions.append(pos[i])
                mag = math.sqrt((vel[i][0]**2)+(vel[i][1]**2)+(vel[i][2]**2))
                Velocities.append(mag)
        except:
            print ("Error reading file at time...t = " + str(j)) 
            # standard error message is unhelpful, easier to locate with time   
    
#    create zero'd matrix to hold data     #   
            
#range of x and y is between -0.025 and 0.025
#1 mm divisions + 2mm padding around outside for visual  
    spacing = 100 
    boarder = 4  
    maxV = 0.025 
    padding = 2
    grid = []
    for i in range (0, spacing + boarder):
        row = []
        for j in range (0, spacing + boarder):
            row.append([])
        grid.append(row)
        

#    Fill grid with all values    #    
    for i in range(0, len(Positions)):
        temp1 = Positions[i][0]
        temp2 = Positions[i][1]
        v = Velocities[i]
        x = int((temp1 + maxV) * (spacing * 10 * 2)) + padding # produce an integer value and add padding
        y = int((temp2 + maxV) * (spacing * 10 * 2)) + padding
        grid[y][x].append(v)

#    Average velocity of a cell    #
        
    def Average(arr):
        if(len(arr) == 0):
            return float('NaN') # catch empty arrays, and set 0 to NaN for mask function 
        else:
            return sum(arr)/len(arr)
    
    for y in range(0, len(grid)):
        for x in range(0,len(grid[y])):
            grid[y][x] = Average(grid[y][x])
     
    return(grid)
  
#-------------------#
#  create heatmap   #
#-------------------#

g1 = Heatmap(d1,t1, t1 + 300)

#-----------------#
#  set map color  #
#-----------------#

cmap = sb.cubehelix_palette(start = 3, rot = -0.1, light = 0.8, dark = 0.1, as_cmap=True)

#----------------#
#   draw maps    #
#----------------#

df = pd.DataFrame(g1)
mask = df.isnull()
fig = plt.figure(1)
ax = sb.heatmap(g1, vmax = 40, cmap=cmap, mask=mask, xticklabels=False, yticklabels=False, linewidth = 0.0, cbar_kws={'label': 'Velocity (m/s)'})
ax.invert_yaxis() 
fig.show()
