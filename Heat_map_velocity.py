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
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from matplotlib.colors import ListedColormap
import matplotlib as mpl
'''
#-----------------#
#    Load data    # 
#-----------------#
d1 = Deck("0.4g/0.4g.dem")
d2 = Deck("0.8g/0.8g.dem")
d3 = Deck("1.2g/1.2g.dem")
d4 = Deck("1.6g/1.6g.dem")
d5 = Deck("2.0g/2.0g.dem")

#-----------------#
#  get timesteps  #
#-----------------#
t1 = d1.numTimesteps - 301
t2 = d2.numTimesteps - 301
t3 = d3.numTimesteps - 301
t4 = d4.numTimesteps - 301
t5 = d5.numTimesteps - 301


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
#0.5 mm divisions + 2mm padding around outside for visual  
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
#  create heatmaps  #
#-------------------#

g1 = Heatmap(d1,t1, t1 + 300)
g2 = Heatmap(d2,t2, t2 + 300)
g3 = Heatmap(d3,t3, t3 + 300)
g4 = Heatmap(d4,t4, t4 + 300)
g5 = Heatmap(d5,t5, t5 + 300)
'''
#-----------------#
#  set map color  #
#-----------------#
# examples of cmap calls
#cmap = sb.cubehelix_palette(start = 3.3, rot = 0.1, gamma = 0.8, light = 0.90, dark = 0.2, as_cmap=True)
#cmaps = cmap('Sequential', ['Oranges'])
my_cmap = plt.cm.Spectral_r(np.arange(plt.cm.Spectral_r.N))

# Alpha blending example #
a = 1.0  #<- change alpha to some fraction i.e. 0.8
my_cmap[:,0:1] *= a 
my_cmap = ListedColormap(my_cmap)

# No longer needed with color shift function
def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'): # default values
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero.

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower offset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax / (vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highest point in the colormap's range.
          Defaults to 1.0 (no upper offset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }
       # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = mpl.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap
shrunk_cmap = shiftedColorMap(my_cmap, start=0.0, midpoint=0.35, stop=1.0, name='shrunk')
#----------------#
#   draw maps    #
#----------------#

df = pd.DataFrame(g1)
mask = df.isnull()
fig = plt.figure(1)
ax = sb.heatmap(g1, vmax = 30, cmap=shrunk_cmap,  mask=mask, xticklabels=False, yticklabels=False,linewidth = 0.0, cbar_kws={'label': 'Velocity (m/s)'})
ax.invert_yaxis() 
fig.show()

df = pd.DataFrame(g2)
mask = df.isnull()
fig = plt.figure(2)
ax = sb.heatmap(g2, vmax = 30, cmap=shrunk_cmap,  mask=mask, xticklabels=False, yticklabels=False, linewidth = 0.0, cbar_kws={'label': 'Velocity (m/s)'})
ax.invert_yaxis() 
fig.show()

df = pd.DataFrame(g3)
mask = df.isnull()
fig = plt.figure(3)
ax = sb.heatmap(g3, vmax = 30, cmap=shrunk_cmap,  mask=mask, xticklabels=False, yticklabels=False, linewidth = 0.0, cbar_kws={'label': 'Velocity (m/s)'})
ax.invert_yaxis()
fig.show()

df = pd.DataFrame(g4)
mask = df.isnull()
fig = plt.figure(4)
ax = sb.heatmap(g4, vmax = 30, cmap=shrunk_cmap,  mask=mask, xticklabels=False, yticklabels=False, linewidth = 0.0, cbar_kws={'label': 'Velocity (m/s)'})
ax.invert_yaxis() 
fig.show()

df = pd.DataFrame(g5)
mask = df.isnull()
fig = plt.figure(5)
ax = sb.heatmap(g5, vmax = 30, cmap=shrunk_cmap,  mask=mask, xticklabels=False, yticklabels=False, linewidth = 0.0, cbar_kws={'label': 'Velocity (m/s)'})
ax.invert_yaxis() 
fig.show()

'''
#------------#
# line plots #
#------------#
def avePoints(p, x, y, z):
    if math.isnan(p) == True:
        p = 0
    if math.isnan(x) == True:
        x = 0
    if math.isnan(y) == True:
        y = 0
    if math.isnan(z) == True:
        z = 0
    
    return((p+x+y+z)/4)
   

def vData(grid):
    line = []
    xPos = 14
    yPos = 14
    length = int((len(grid)-4)/2)+1
    for j in range(0, length): # only need half the mill
        p = grid[yPos][xPos]
        x = grid[yPos][xPos+1]
        y = grid[yPos+1][xPos]
        z = grid[yPos+1][xPos+1]
        line.append(avePoints(p,x,y,z))
        xPos += 1
        yPos += 1
        
    return line

l1 = vData(g1)
l1.pop(0)
l2 = vData(g2)
l2.pop(0)
l3 = vData(g3)
l3.pop(0)
l4 = vData(g4)
l4.pop(0)
l5 = vData(g5)
l5.pop(0)


xmarks = np.arange(0.25,25,0.5)
#xmarks = np.insert(xmarks,0,0)
    
fig, ax = plt.subplots()
ax.plot(xmarks,l1, label = "0.4g")
ax.plot(xmarks,l2, label = "0.8g")
ax.plot(xmarks,l3, label = "1.2g")
ax.plot(xmarks,l4, label = "1.6g")
ax.plot(xmarks,l5, label = "2.0g")
plt.xlabel('Distance from outer wall (mm)')
plt.ylabel("Velocity (m/s)")
plt.grid(which='major', axis='y', linestyle='--')
#axins = zoomed_inset_axes(ax, 1.4, loc=5)
#axins.plot(xmarks,l1)
#axins.plot(xmarks,l2)
#axins.plot(xmarks,l3)
#axins.plot(xmarks,l4)
#axins.plot(xmarks,l5)
#x1, x2, y1, y2 = 0, 6, 0, 6 # specify the limits
#axins.set_xlim(x1, x2) # apply the x-limits
#axins.set_ylim(y1, y2) # apply the y-limits
#mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
ax.legend()
'''